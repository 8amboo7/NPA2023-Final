from ncclient import manager
import xmltodict

m = manager.connect(
    host="10.0.15.181",
    port=830,
    username="admin",
    password="cisco",
    hostkey_verify=False
    )

def create():
    netconf_config = """
    <config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>Loopback65070211</name>
                <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:softwareLoopback</type>
                <enabled>true</enabled>
                <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                    <address>
                        <ip>
                        172.30.211.1
                        </ip>
                        <netmask>  
                        255.255.255.0
                        </netmask>
                    </address>
                </ipv4>
                <ipv6 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip"/>
            </interface>
        </interfaces>
    </config>
                    """
    try:
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return "Interface loopback65070211 is created successfully"
    except Exception as e:
        print(e)
        print("Error!")
        return "Cannot create: Interface loopback65070211"


def delete():
    netconf_config = """
    <config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface operation="delete">
                <name>Loopback65070211</name>
            </interface>
        </interfaces>
    </config>
                    """

    try:
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return "Interface loopback65070211 is deleted successfully"
    except:
        print("Error!")
        return "Cannot delete: Interface loopback65070211"


def enable():
    netconf_config = """
    <config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>Loopback65070211</name>
                <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:softwareLoopback</type>
                <enabled>true</enabled>
            </interface>
        </interfaces>
    </config>
                    """

    try:
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return "Interface loopback65070211 is enabled successfully"
    except:
        print("Error!")
        return "Cannot enable: Interface loopback65070211"


def disable():
    netconf_config = """
    <config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>Loopback65070211</name>
                <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:softwareLoopback</type>
                <enabled>false</enabled>
            </interface>
        </interfaces>
    </config>
                    """

    try:
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return "Interface loopback65070211 is shutdowned successfully"
    except:
        print("Error!")
        return "Cannot shutdown: Interface loopback65070211"

def netconf_edit_config(netconf_config):
    return  m.edit_config(target="running", config=netconf_config)
    

def status():
    netconf_filter = """
    <filter>
        <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>Loopback65070211</name> <!-- Replace with your specific interface name -->
            </interface>
        </interfaces-state>
    </filter>
                    """

    try:
        # Use Netconf operational operation to get interfaces-state information
        netconf_reply = m.get(filter=netconf_filter)
        print(netconf_reply)
        netconf_reply_dict = xmltodict.parse(netconf_reply.xml)

        # if there data return from netconf_reply_dict is not null, the operation-state of interface loopback is returned
        interface_data = netconf_reply_dict.get("rpc-reply", {}).get("data", {}).get("interfaces-state", {}).get("interface", {})
        if (interface_data):
            # extract admin_status and oper_status from netconf_reply_dict

            admin_status = interface_data.get("admin-status")
            oper_status = interface_data.get("oper-status")

            if admin_status == 'up' and oper_status == 'up':
                return "nterface loopback65070211 is enabled"
            elif admin_status == 'down' and oper_status == 'down':
                return "Interface loopback65070211 is disabled"
        else: # no operation-state data
            return "No Interface loopback65070211"
    except:
        print("Error!")
