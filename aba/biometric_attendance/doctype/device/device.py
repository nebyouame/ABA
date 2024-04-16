# Copyright (c) 2024, TTSP and contributors
# For license information, please see license.txt

import frappe
import requests
from requests.auth import HTTPDigestAuth
from frappe.model.document import Document

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

class Device(Document):
	def before_save(self):
		stat = device_status(self.user_name,self.password,self.ip_address)
		if stat != "Online":
			frappe.throw("The device is offline")
		else:
			pass
