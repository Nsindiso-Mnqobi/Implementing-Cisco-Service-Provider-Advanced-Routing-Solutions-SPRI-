from ncclient import manager                                                                       
from credentials  import credentials
import csv
import xmltodict 
import json

class  configure_bgp:                                                                                               # Create Class
    device_ip=""                                                                                                        
    router_id= ""
    device_asn= ""
    remote_ip = "" 
    remote_asn = "" 
    description = ""

    def __init__(self, device_ip, router_id, device_asn, remote_ip, remote_asn, description ):
        self.host= device_ip
        self.router_id = router_id
        self.device_asn = device_asn
        self.remote_ip = remote_ip
        self.remote_asn = remote_asn
        self.description = description
    
    def configure_device(self):

        with manager.connect(host = self.host, port = credentials['port'], 
                                            username=credentials['username'], password= credentials['password'], 
                                            hostkey_verify=False,device_params={'name':'iosxe'}) as device:                                                                 # Connect to device.
            
            with device.locked("running"):                                                                                                                                                        # lock runnung config during transaction.
                config_template = open('Config-template.xml').read()                                                                                                                # Open Config template cotaining YANG Module.
                netconf_config = config_template.format(asn=self.device_asn,
                                                                                    id = self.router_id,
                                                                                    remote_ip = self.remote_ip ,
                                                                                    remote_asn = self.remote_asn,
                                                                                    description = self.description)                                                                                  # Assiging variables to the YANG Module. 
                
                try:                                                                                                                                                                                                  # Error handling
                    device.edit_config(config = netconf_config, target = "running")
                    print( self.host + " :has been configured")
                except:
                    print("An error occured while configuring the device")
                
    def get_config(self):

        with manager.connect(host = self.host, port = credentials['port'], 
                                            username=credentials['username'], password= credentials['password'], device_params={'name':'iosxe'},
                                            hostkey_verify=False) as device:
            
            get_config = open("get_config.xml").read()
            netconf_filter = get_config
            
            subscription_config = device.get(netconf_filter)   
            subscription_parse = xmltodict.parse(subscription_config.xml)["rpc-reply"]["data"]["native"]["router"]["bgp"]["neighbor"]
            print("#"*20 + self.host +"#"*20)
            print("Neighbors_Address"+"*"*5+"remote_as"+"*"*10+"description") 
            
            for item in subscription_parse:
                try:
                    print(item["id"]+"*"*16+item["remote-as"]+"*"*10+item["description"])
                except:
                    print(subscription_parse["id"]+"*"*16+subscription_parse["remote-as"]+"*"*10+subscription_parse["description"])
                    print("")
                    break
            print("")
      
if  __name__ == "__main__":

    with open("config_variable.csv") as host_details:
        config_variable = list(csv.reader(host_details))
        for row in config_variable:
            device_ip=row[0]
            router_id= row[1]
            device_asn=row[2]
            remote_ip = row[3] 
            remote_asn = row[4] 
            description = row[5]
            Config = configure_bgp(device_ip, router_id, device_asn, remote_ip, remote_asn, description)
            Config.configure_device()            
            Config.get_config()



