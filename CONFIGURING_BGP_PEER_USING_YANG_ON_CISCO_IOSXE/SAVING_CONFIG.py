from ncclient import manager
from ncclient import xml_
from credentials import credentials
import csv
import xmltodict
import json


class save_config:
    device_ip = ""
    router_id = ""
    device_asn = ""
    remote_ip = ""
    remote_asn = ""
    description = ""

    def __init__(self, device_ip):
        self.host = device_ip

    def save_config(self):

        with manager.connect(host=self.host, port=credentials['port'],
                             username=credentials['username'], password=credentials['password'],
                             hostkey_verify=False, device_params={'name': 'iosxe'}) as device:

            save_body = """ 
            <cisco-ia:save-config xmlns:cisco-ia="http://cisco.com/yang/cisco-ia"/>
            """
            save_rpc = device.dispatch(xml_.to_ele(save_body))
            save_reply = xmltodict.parse(save_rpc.xml)
            reply = self.host + " : " + \
                save_reply["rpc-reply"]["result"]["#text"]
            print(reply)

if __name__ == "__main__":

    with open("config_variable.csv") as host_details:
        config_variable = list(csv.reader(host_details))
        for row in config_variable:
            device_ip = row[0]
            config = save_config(device_ip)
            config.save_config()
