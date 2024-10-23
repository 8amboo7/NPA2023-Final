import json
import requests
requests.packages.urllib3.disable_warnings()

# Router IP Address is 10.0.15.189
api_url = "https://10.0.15.182/restconf"

# the RESTCONF HTTP headers, including the Accept and Content-Type
# Two YANG data formats (JSON and XML) work with RESTCONF 
headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}
basicauth = ("admin", "cisco")

def check_interface_exists(loopback_name):
    resp = requests.get(
        f"{api_url}/data/ietf-interfaces:interfaces/interface={loopback_name}",
        auth=basicauth,
        headers=headers,
        verify=False
    )
    return resp.status_code == 200


def create(studentID):
    # ตั้งชื่อ Loopback interface ตาม studentID
    loopback_name = f"Loopback65070211"
    # ใช้เลข 3 หลักสุดท้ายของ studentID ในการตั้งค่า IP Address
    ip_last_octet = studentID[-3:]
    ip_address = f"172.30.{ip_last_octet}.1"
    
    # ตรวจสอบก่อนว่า Loopback interface นั้นมีอยู่แล้วหรือไม่
    if not check_interface_exists(loopback_name):
        # ถ้าไม่มี interface อยู่ จะสร้างใหม่โดยใช้ YANG model
        yangConfig = {
            "ietf-interfaces:interface": {
                "name": loopback_name,
                "description": f"Loopback interface for student {studentID}",
                "type": "iana-if-type:softwareLoopback",
                "enabled": True,
                "ietf-ip:ipv4": {
                    "address": [
                        {
                            "ip": ip_address,
                            "netmask": "255.255.255.0"
                        }
                    ]
                }
            }
        }

        # ส่ง POST request ไปยัง RESTCONF API เพื่อสร้าง interface
        resp = requests.post(
            f"{api_url}/data/ietf-interfaces:interfaces",
            data=json.dumps(yangConfig),  # แปลงข้อมูลเป็น JSON
            auth=basicauth,  # ข้อมูลการ authentication
            headers=headers,  # HTTP headers
            verify=False  # ไม่ตรวจสอบ SSL certificate
        )

        # ตรวจสอบสถานะการสร้าง interface
        if resp.status_code == 201:  # 201 คือ สร้างสำเร็จ
            return f"Interface {loopback_name} is created successfully"
        else:
            return f"Error creating interface: {resp.status_code}"
    else:
        # ถ้ามี Interface อยู่แล้ว ไม่ต้องสร้างใหม่
        return f"Cannot create: Interface {loopback_name} already exists"


def delete(studentID):
    loopback_name = f"Loopback{studentID}"
    
    if check_interface_exists(loopback_name):
        resp = requests.delete(
            f"{api_url}/data/ietf-interfaces:interfaces/interface={loopback_name}",
            auth=basicauth,
            headers=headers,
            verify=False
        )
        if resp.status_code == 204:
            return f"Interface {loopback_name} is deleted successfully"
        else:
            return f"Error deleting interface: {resp.status_code}"
    else:
        return f"Cannot delete: Interface {loopback_name} does not exist"

def enable(studentID):
    loopback_name = f"Loopback{studentID}"
    
    if check_interface_exists(loopback_name):
        yangConfig = {
            "ietf-interfaces:interface": {
                "enabled": True
            }
        }

        resp = requests.put(
            f"{api_url}/data/ietf-interfaces:interfaces/interface={loopback_name}",
            data=json.dumps(yangConfig),
            auth=basicauth,
            headers=headers,
            verify=False
        )

        if resp.status_code == 204:
            return f"Interface {loopback_name} is enabled successfully"
        else:
            return f"Error enabling interface: {resp.status_code}"
    else:
        return f"Cannot enable: Interface {loopback_name} does not exist"



def disable(studentID):
    loopback_name = f"Loopback{studentID}"
    
    if check_interface_exists(loopback_name):
        yangConfig = {
            "ietf-interfaces:interface": {
                "enabled": False
            }
        }

        resp = requests.put(
            f"{api_url}/data/ietf-interfaces:interfaces/interface={loopback_name}",
            data=json.dumps(yangConfig),
            auth=basicauth,
            headers=headers,
            verify=False
        )

        if resp.status_code == 204:
            return f"Interface {loopback_name} is shutdowned successfully"
        else:
            return f"Error disabling interface: {resp.status_code}"
    else:
        return f"Cannot shutdown: Interface {loopback_name} does not exist"

def status(studentID):
    loopback_name = f"Loopback{studentID}"

    if check_interface_exists(loopback_name):
        resp = requests.get(
            f"{api_url}/data/ietf-interfaces:interfaces/interface={loopback_name}",
            auth=basicauth,
            headers=headers,
            verify=False
        )
        if resp.status_code == 200:
            response_json = resp.json()
            admin_status = response_json["ietf-interfaces:interface"]["enabled"]
            oper_status = response_json["ietf-interfaces:interface"]["ietf-ip:ipv4"]["enabled"]
            if admin_status and oper_status == 'up':
                return f"Interface {loopback_name} is enabled"
            else:
                return f"Interface {loopback_name} is disabled"
        else:
            return f"Error getting status: {resp.status_code}"
    else:
        return f"No Interface {loopback_name}"