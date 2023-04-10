import requests
import time

proposer = 'http://127.0.0.1:9860'

latest = -1
diffs = []
while True:
    res = requests.get(f'{proposer}/read_latest')
    code = res.status_code
    if code != 200:
        print(f"Proposer not responding. Test terminated. average latency: {sum(diffs)/len(diffs)}")
    ts = res.json()
    ts = float(ts)
    if ts > latest:
        latest = ts
        now = time.time()
        diffs.append(now - ts)
        print(diffs[-1])