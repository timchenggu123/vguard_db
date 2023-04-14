import requests
import time
from time import sleep

proposer = 'http://127.0.0.1:9860'

latest = -1
diffs = []
# while True:
#     res = requests.get(f'{proposer}/read_latest')
#     code = res.status_code
#     if code == 200:
#         print(f"Proposer not responding. Waiting...")
#         break
    
for i in range(10):
    while True:
        sleep(0.1)
        try:
            res = requests.get(f'{proposer}/read_latest')
            ts = res.json()
        except:
            continue
        ts = float(ts)
        if ts > latest:
            latest = ts
            now = time.time() * 1e6
            diffs.append(now - ts)
            print(diffs[-1])
            break
        
print(f'Test finished. Average latency is {sum(diffs)/len(diffs) * 1e6} seconds')
