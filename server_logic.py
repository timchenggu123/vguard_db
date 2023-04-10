from time import sleep
import random

import mysql.connector
import requests
import json

class Server():
    def __init__(self,app):
        self.app = app
        self.is_backup=False
        self.backup_list={
            "active":[],
            "obsolete":[],
            "id": 0
        }
        self.offline=False
        self.backup_list_id = 0
         
    @property
    def proposer_id(self):
        return self.app.config['proposer_id']
        
    @property
    def is_proposer(self):
        return self.app.config['is_proposer']

    @property
    def id(self):
        return self.app.config['id']
    
    @property
    def log_file(self):
        return self.app.config['log_file']

    @property
    def address(self):
        return self.app.config['address']
    
    @property
    def k_backups(self):
        return self.app.config['k_backups']
    
    ##======== helper function==============
    
    def _db_insert_data(self,conn,table,data):
        cursor = conn.cursor()
        #cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED")
        try:
            cursor.execute(f"INSERT IGNORE INTO {table} VALUES ({','.join(['%s' for i in range(len(data))])})", data)
            conn.commit()

        except mysql.connector.errors.DatabaseError as e:
            # handle the deadlock error
            if 'Deadlock found' in str(e):
                print("Deadlock found when trying to get lock; retrying transaction")
                conn.rollback()
                # retry the transaction or take other corrective actions
            else:
                raise e

        
    def _db_read_all(self, conn, table):
        cursor = conn.cursor(buffered=True)
        #cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED")
        cursor.execute(f"SELECT * FROM {table}")
        # fetch all the rows and store them in a list of dictionaries
        rows = cursor.fetchall()
        out = []
        for d in rows:
            out.append([i for i in d])
        return out

    def _db_read_latest_timestamp(self, conn,table):
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {table} ORDER BY timestamp DESC LIMIT 1")
        # fetch all the rows and store them in a list of dictionaries
        rows = cursor.fetchall()
        for d in rows:
            out = d['timestamp']
        return out

    ##======== Non proposer logic===========
    def on_chosen_as_backup(self, data, conn):
        
        if self.is_proposer:
            raise TypeError('Proposer cannot be chosen as backup')
        self.delete_backup(conn)
        self.is_backup=True
        return self.make_replica(data, conn)
        
    def make_replica(self,data,conn):
        '''
        Copy the data into the database
        '''
        table = 'gps_data'
        # clean existing data
        c=conn.cursor()
        try:
            c.execute(f"DELETE FROM {table};")
            conn.commit()
        except mysql.connector.errors.DatabaseError as e:
            # handle the deadlock error
            if 'Deadlock found' in str(e):
                print("Deadlock found when trying to get lock; retrying transaction")
                conn.rollback()
                # retry the transaction or take other corrective actions
            else:
                raise e
        # replicate the changes on the non-proposer
        for row in data:
            self._db_insert_data(conn, table, row)
        return True
    
    
    def on_requested_delete_obsolete(self, backup_list, conn):
        if self.backup_list['id'] > backup_list['id']:
            raise ValueError()
        self.backup_list=backup_list
        self.is_backup=False
        self.delete_backup(conn)
        
    def delete_backup(self, conn):
        '''
        delete the backup data
        '''
        table='gps_data'
        c = conn.cursor()
        c.execute(f"DELETE FROM {table};")
        conn.commit()
        return True
    
    def on_requested_read(self, query, conn):
        '''
        When a this server receives a request of reading data from its backup database
        '''
        if self.is_backup or self.is_proposer:
            #read data
            cursor = conn.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            out = []
            for d in data:
                out.append([i for i in d])
            return out, None
        else:
            return None, self.backup_list['active']
    
    def on_requested_update_backup_list(self, backup_list):
        if self.backup_list['id'] >= backup_list['id']:
            raise ValueError()
        '''
        when receiving a request to update backup list
        '''
        self.backup_list=backup_list
        
    def read_data(self, query):
        '''
        read data
        '''
        response = self.request_data(query, [self.proposer_id]) #query is some SQL query
        if response.status_code == 200:
            data = response.json()['data']
            if data is not None:
                return data
            
        backup_ids = self.backup_list['active']    
        while True:
            response = self.request_data(query, backup_ids) #if success, returns the same backup_ids as input; otherwise, returns new backup_ids
            if response.status_code == 200:
                if response.json()['data'] is not None:
                    data=response.json()['data']
                    break
                backup_ids = response.json()['new_backup_ids']
                
        return data
    
    def request_data(self, query, ids):
        '''
        request data from multiple destination ids
        '''
        status = False
        for id in ids:
            #request data, or get the new backup_ids from response
            ip,port = self.address[id]
            response = requests.get(f'{ip}:{port}/read', json={'query':query})
            status = response.status_code == 200
            if status:
                return response
        return response
            
    ##=======Proposer logic==========
    
    def on_end_of_booth(self, data, conn):
        if self.is_proposer:
            self.make_backups(data, conn)
            
    def make_backups(self,data, conn):
        status = False
        participants = data['participants']
        while not status:
            status, chosen = self.choose_random_backups(participants, conn)
            if not status:
                continue
            status = self.broadcast_backups_to_booth(chosen, participants)
            self.update_backup_list(chosen)
            print(f"The backup list is {self.backup_list['obsolete']}")
            self.request_delete_obsolete()
            print(f"The chosen is {chosen}")

    def choose_random_backups(self,participants, conn):
        chosen = random.sample(participants, k=self.k_backups)
        for c in chosen:
            response = self.request_to_be_backups(c, conn)
            if response.status_code != 200:
                return False, None
        return True, chosen
    
    def request_to_be_backups(self,chosen, conn):
        '''
        request the chosen vehicles to be backup

        '''
        ip,port = self.address[chosen]
        data=self._db_read_all(conn, 'gps_data')
        response = requests.post(f'{ip}:{port}/choose_backup', json=data)
        return response
    
    def broadcast_backups_to_booth(self, chosen, participants):
        '''
        Inform all of the participant of the booth which are the backup
        '''
        for i in participants:
            ip,port = self.address[i]
            response = requests.post(f'{ip}:{port}/update_backup_list', json=chosen)
            if response.status_code!=200:
                return False
        return True
    
    def update_backup_list(self, chosen):
        old_active = self.backup_list['active']
        self.backup_list['obsolete']+=old_active
        self.backup_list['obsolete'] = [x for x in self.backup_list['obsolete'] if x not in chosen]
        self.backup_list['obsolete'] = list(dict.fromkeys(self.backup_list['obsolete']))
        self.backup_list['active'] = chosen
        if self.is_proposer:
            self.backup_list['id'] = self.backup_list_id
            self.backup_list_id += 1
    
    def request_delete_obsolete(self):
        '''
        request the obsolete backups to delete their data
        '''
        obsoletes = [i for i in self.backup_list['obsolete']]
        for i in obsoletes:
            ip,port = self.address[i]
            response = requests.post(f'{ip}:{port}/delete_obsolete', json=self.backup_list)
            if response.status_code == 200:
                try:
                    self.backup_list['obsolete'].remove(i)
                except ValueError:
                    print(f"The requested obsolete {i} is not in the backup list")
                    print(obsoletes)
                    print(self.backup_list['obsolete'])
                    continue
        return True
        
    def get_vehicle_address(self, id):
        return self.vehicle_id_address[id]

    
if __name__ == "__main__":
    server = Server()