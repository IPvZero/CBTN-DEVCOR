"""
AUTHOR: IPvZero
"""

import requests
import xmltodict
from rich import print as rprint

prefix = input("Enter the Prefix/Server Name you want to create: ")
instances = input("Enter the number of instances you would like to create: ")

log_resp = requests.post(
    "http://10.10.20.113/nuova",
    headers={"Content-Type": "application/x-www-form-urlencoded"},
    data='<aaaLogin inName="ucspe" inPassword="ucspe"/>',
)

log_output = xmltodict.parse(log_resp.text)
real_cookie = log_output["aaaLogin"]["@outCookie"]

request = f"""
<lsInstantiateNTemplate
    dn="org-root/ls-johntemplate"
    cookie="{real_cookie}"
    inTargetOrg="org-root"
    inServerNamePrefixOrEmpty="{prefix}"
    inNumberOf="{instances}"
    inHierarchical="no">
</lsInstantiateNTemplate>
"""

req_resp = requests.post(
    "http://10.10.20.113/nuova",
    headers={"Content-Type": "application/x-www-form-urlencoded"},
    data=f"{request}",
)

req_resp.raise_for_status()
req_output = xmltodict.parse(req_resp.text)
looper = req_output["lsInstantiateNTemplate"]["outConfigs"]["lsServer"]
for server in looper:
    parse_template = server["@srcTemplName"]
    parse_name = server["@name"]
    parse_id = server["@intId"]
    rprint(
        f"Server {parse_name} has been created (ID: {parse_id})"
        f"- based on the {parse_template} template"
    )
