from time import sleep
import random

class Server():
    vehicle_id_address = {}
    def __init__(self, id, proposer=False, proposer_id = 0, log_file=f'./logs/id.txt', config=None):
        self.is_proposer = proposer
        self.is_backup = False
        self.proposer_id= self.proposer_id
        self.id = InterruptedError
        self.log_file = log_file
        self.config=config
        self.backup_list = {
            "obsolete":[],
            "active":[]
        }
    
    def run(self):
        while True:
            self.check_log_updated()
            sleep(10)
            pass
    
    def check_log_updated(self):
        # check if log is updated
        with open(self.log_file, 'r') as f:
            initial = f.read()
            while True:
                current = f.read()
                if initial != current:
                    for line in current:
                        if line not in initial:
                            data = line
                    break
        
        #log is updated, meaning a booth just ended. We proceed with logic.
        self.on_end_of_booth(data)
    
    def on_end_of_booth(self, data):
        if self.is_proposer:
            self.make_backups(data)
    
    ##======== Non proposer logic===========
    
    def on_chosen_as_backup(self, data):
        if self.is_proposer:
            return False
        
        self.is_backup=True
        return self.make_replicata(self)
        
    def make_replica(self,data):
        '''
        Copy the data into the database
        TODO: Not Implemented
        '''
        return True
    
    def on_requested_delete_obsolete(self, backup_list):
        '''
        TODO: WIP
        '''
        self.backup_list=backup_list
        self.is_backup=False
        self.delete_backup()
        
    def delete_backup():
        '''
        delete the backup data
        TODO: Not Implemented
        '''
        return True
    
    def on_requested_data(self, query):
        '''
        When a request is sent to read data from the backup database
        TODO: WIPs
        '''
        if self.is_backup:
            #read data
            raise NotImplementedError()
        else:
            return self.backup_list()
    
    def on_requested_update_backup_lsit(self, backup_list):
        '''
        when receiving a request to update backup list
        '''
        self.backup_list=backup_list
        
    def read_data(self, query):
        '''
        read data
        TODO: Not Implemented
        '''
        try:
            self.request_data(query, [self.proposer_id]) #query is some SQL query
        except:
            backup_ids = self.backup_list['active']
            while status != 'SUCCESS':
                status, new_backup_ids, data = self.request_data(query, [backup_ids]) #if success, returns the same backup_ids as input; otherwise, returns new backup_ids
                backup_ids = new_backup_ids
        return data
    
    def request_data(self, ids):
        '''
        request data from multiple destination ids
        TODO: WIP
        '''
        new_backup_ids = None
        status = False
        for id in ids:
            #request data, or get the new backup_ids from response
            pass
        
        return status, new_backup_ids
            
    ##=======Proposer logic==========
    
    def make_backups(self,data):
        status = False
        participants = self.get_vehicles_from_log_entry(data)
        while not status:
            status, chosen = self.choose_random_backups(participants)
            status &= self.broadcast_backups_to_booth(chosen, participants)
            self.update_backup_list(chosen)
            status &= self.request_delete_obsolete()

    def choose_random_backups(self,participants):
        
        chosen = random.choices(participants, k=self.config['k_backups'])
        status = self.request_to_be_backups(chosen)
        return status, chosen
        
    def request_to_be_backups(self,chosen):
        '''
        request the chosen vehicles to be backup
        TODO: implement
        '''
        return True
        
    def get_vehicles_from_log_entry(self, data):
        '''
        Given the newest line of the log entry, extract the paticipant vehicles ids from it
        TODO: implement
        '''
        raise NotImplementedError
    
    def broadcast_backups_to_booth(self, chosen, participants):
        '''
        Inform all of the participant of the booth which are the backup
        TODO: implement
        '''
        return True
    
    def update_backup_list(self, chosen):
        old_active = self.backup_list['active']
        self.backup_list['obsolete'].append(old_active)
        self.backup_list['obsolete'] = [x for x in self.backup_list['obsolete'] if x not in chosen]
                
        self.backup_list['active'] = chosen
    
    def request_delete_obsolete(self):
        '''
        request the obsolete backups to delete their data
        TODO:implement
        '''
        return True
        
    def get_vehicle_address(self, id):
        return self.vehicle_id_address[id]

    
if __name__ == "__main__":
    server = Server()