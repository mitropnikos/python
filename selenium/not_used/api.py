import json
import requests
from collections import Counter

response = requests.get("*****")
a= response.json()
p = json.dumps(a)
resp = json.loads(p)

c = len(Counter(resp['accountName'] for resp in resp))

print(c)
a  = 0

while a < c:
    
    print(resp[a]["tlcs"],resp[a]["environments"][0]["deployments"][0]["host"])
    a += 1
