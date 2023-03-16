import requests

# Add a new data
response = requests.post('http://localhost:5000/data', json={'foo': '123', 'bar': 'abc'})
if response.status_code == 201:
    print('Data added successfully!')
else:
    print('Failed to add user.')

# Retrieve all data
response = requests.get('http://localhost:5000/data')
if response.status_code == 200:
    print('Data:')
    for data in response.json()['data']:
        print('  - ID:', data['id'])
        print('    foo:', data['foo'])
        print('    bar:', data['bar'])
else:
    print('Failed to retrieve data.')