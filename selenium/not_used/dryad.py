import requests
import uuid
import json

class Dryad():

#class object attributes    
    global uuid 
  
    uuid = str(uuid.uuid4())
    

    

    def __init__(self):1
        self.self = self
    


    #activate user 
    def activate_user(hostname,subscriptionId,subscriptionScheme,number,old_dcs='no'):
             
            lh = '****/activate'
            mn = '****/activate'
            a = zervas2
            host  = hostname[:2]
            sub =  subscriptionId
            scheme = subscriptionScheme
            msisdn = number
            dcs = old_dcs

            if  host  == 'lh':
                host = 'http://'+hostname+'.'+lh
                print (host)
            elif host  == 'md':
                host = 'http://'+hostname+'.'+mn
            else:
                print ('something wrong with host')

   
            request_headers = {'Content-Type': 'application/json'}
            
            payload = {
                        "ctxId": uuid,
                        "payment": {
                            "metadata": {},
                            "method": "MNO"
                        },
                        "subscriptionId": sub ,
                        "subscriptionMetadata": {},
                        "subscriptionScheme": scheme,
                        "user": {
                            "id":  msisdn,
                            "type": "MSISDN"
                        },
                        "origin": "SMS",
                        "uid": uuid,
                        "metadata": {}
            }


            payload_transformation = json.dumps(payload)
            request = requests.post(host, data=payload_transformation, headers=request_headers)  
               
            
            


            return request.content



#cancelled user
         
    def cancel_user(hostname,subscriptionId,subscriptionScheme,number,old_dcs='no'):

            lh = '****/cancel'
            mn = '****/cancel'

            host  = hostname[:2]
            sub =  subscriptionId
            scheme = subscriptionScheme
            msisdn = number
            dcs = old_dcs

            if  host  == 'lh':
                host = 'http://'+hostname+'.'+lh
                print (host)
            elif host  == 'md':
                host = 'http://'+hostname+'.'+mn
            else:
                print ('something wrong with host')

   
            request_headers = {'Content-Type': 'application/json'}
            
            payload = {
                        "ctxId": uuid,
                        "payment": {
                            "metadata": {},
                            "method": "MNO"
                        },
                        "subscriptionId": sub ,
                        "subscriptionMetadata": {},
                        "subscriptionScheme": scheme,
                        "user": {
                            "id":  msisdn,
                            "type": "MSISDN"
                        },
                        "origin": "SMS",
                        "uid": uuid,
                        "metadata": {}
            }


            payload_transformation = json.dumps(payload)
            request = requests.post(host, data=payload_transformation, headers=request_headers)  
               
            
            


            return request.content



#reset user


a = Dryad.cancel_user('****','****','****','****')
print(a)
