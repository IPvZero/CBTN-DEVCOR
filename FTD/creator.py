import requests
import json
from rich import print

requests.packages.urllib3.disable_warnings()
url = "https://10.10.20.65/api/fdm/v5/fdm/token"

payload = {"grant_type": "password", "username": "admin", "password": "Cisco1234"}
headers = {"Accept": "application/json", "Content-Type": "application/json"}

token_response = requests.post(
    url, headers=headers, data=json.dumps(payload), verify=False
)
token_response.raise_for_status()
if token_response.status_code == 200:
    print("Token Successfully Received...\n")

token = token_response.json()["access_token"]

url = "https://10.10.20.65/api/fdm/v5/object/networks"

payload = {
    "name": "IPvZero",
    "description": "DEVCOR",
    "subType": "NETWORK",
    "value": "99.99.99.0/24",
    "dnsResolution": "IPV4_ONLY",
    "type": "networkobject",
}

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": f"Bearer {token}",
}

create_response = requests.post(
    url, headers=headers, data=json.dumps(payload), verify=False
)
create_response.raise_for_status()
if create_response.status_code == 200:
    print("[u]SUCCESS: New Object Created")
    print(create_response.text)
