import json
import requests
requests.packages.urllib3.disable_warnings()


# Router IP Address is 10.0.15.189
api_url = "https://10.0.15.181/restconf"

headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json",
}
basicauth = ("admin", "cisco")

def create():
    yangConfig = {"ietf-interfaces:interface": {
        "name": "Loopback65070211",
        "type": "iana-if-type:softwareLoopback",
        "enabled": True,
        "ietf-ip:ipv4": {
            "address": [
                {
                    "ip": "172.30.211.1",
                    "netmask": "255.255.255.0"
                }
            ]
        },
        "ietf-ip:ipv6": {}
    }}

    resp = requests.put(
        api_url + "/data/ietf-interfaces:interfaces/interface=Loopback65070211", 
        data=json.dumps(yangConfig), 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback65070211 is created successfully" 
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot create: Interface loopback65070211" 

def delete():
    resp = requests.delete(
        api_url + "/data/ietf-interfaces:interfaces/interface=Loopback65070211", 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback65070211 is deleted successfully" 
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot deleted: Interface loopback65070211" 

def enable():
    yangConfig = {
        "ietf-interfaces:interface": {
            "name": "Loopback65070211",
            "type": "iana-if-type:softwareLoopback",
            "enabled": True
        }
    }

    resp = requests.patch(
        api_url + "/data/ietf-interfaces:interfaces/interface=Loopback65070211", 
        data=json.dumps(yangConfig), 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback65070211 is enabled successfully" 
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot enable: Interface loopback65070211" 

def disable():
    yangConfig = {
        "ietf-interfaces:interface": {
            "name": "Loopback65070211",
            "type": "iana-if-type:softwareLoopback",
            "enabled": False
        }
    }

    resp = requests.patch(
        api_url + "/data/ietf-interfaces:interfaces/interface=Loopback65070211", 
        data=json.dumps(yangConfig), 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback65070211 is shutdowned successfully" 
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "'Cannot shutdown: Interface loopback65070211" 
    
def status():
    api_url_status = "https://10.0.15.181/restconf/data/ietf-interfaces:interfaces-state/interface=Loopback65070211"

    resp = requests.get(
        api_url_status, 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        response_json = resp.json()
        # print(json.dumps(response_json, indent=4))

        admin_status = response_json["ietf-interfaces:interface"]["admin-status"]
        oper_status = response_json["ietf-interfaces:interface"]["oper-status"]

        if admin_status == 'up' and oper_status == 'up':
            return "Interface loopback65070211 is enabled" 
        elif admin_status == 'down' and oper_status == 'down':
            return "Interface loopback65070211 is disabled" 
    elif(resp.status_code == 404):
        print("STATUS NOT FOUND: {}".format(resp.status_code))
        return "No Interface loopback65070211" 
    else:
        print('Error. Status Code: {}'.format(resp.status_code))