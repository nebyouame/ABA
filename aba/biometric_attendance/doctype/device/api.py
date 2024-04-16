import frappe
import requests
from requests.auth import HTTPDigestAuth

@frappe.whitelist()
def device_status(userName,password,ip):
    url = f"http://{ip}/ISAPI/AccessControl/UserInfo/capabilities?format=json"
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.get(
        url,
        headers=headers,
        auth=HTTPDigestAuth(userName,password)
    )
    
    if response.status_code == 200:
        return "Online"
    else:
        return "Offline"