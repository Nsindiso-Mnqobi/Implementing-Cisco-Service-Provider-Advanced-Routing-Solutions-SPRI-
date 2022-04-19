from ncclient import manager
from credentials import credentials
import csv
import xmltodict
import json

class verify_neighbor:
    device_ip = ""
    router_id = ""
    device_asn = ""
    remote_ip = ""
    remote_asn = ""
    description = ""

    def __init__(self, device_ip):
        self.host = device_ip

    def get_config(self):
    
        with manager.connect(host = self.host, port = credentials['port'], 
                                            username=credentials['username'], password= credentials['password'], device_params={'name':'iosxe'},
                                            hostkey_verify=False) as device:
            
            get_config = open("operational_parameters.xml").read()
            netconf_filter = get_config
            
            bgp_neighbor_state = device.get(netconf_filter)   
            state_parse = xmltodict.parse( bgp_neighbor_state.xml)["rpc-reply"]["data"]["bgp-state-data"]["neighbors"]["neighbor"]
            print("*"*30 + self.host + "*"*30)
            print("Neighbors IP Address"+"*"*10+"Neighbors Description"+"*"*10+"Neighbors Connection State") 

            for item in state_parse:
                 try:
                     print(item["neighbor-id"]+"*"*20+item["description"]+"*"*20+item["session-state"])
                 except:
                     print(state_parse["neighbor-id"]+"*"*20+state_parse["description"]+"*"*20+state_parse["session-state"])
                     break
                     
if __name__ == "__main__":

    with open("config_variable.csv") as host_details:
        config_variable = list(csv.reader(host_details))
        for row in config_variable:
            device_ip = row[0]
            config = verify_neighbor(device_ip)
            config.get_config()
