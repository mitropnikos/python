import json
import requests
headers = {"Authorization": "*****", 
  "scope": "https://www.googleapis.com/auth/drive"}
para = {
    "name": "test.txt",
    "parents":[""*****","]
}
files = {
    'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
    'file': open("./test.txt", "rb")
}
r = requests.post(
    "https://www.googleapis.com/****",
    headers=headers,
    files=files
)
print(r.text)
