import requests
import uuid
import json

class SecureD():

#class object attributes    
   
    def __init__(self):
        self.self = self
    


    #reset user 
    def reset_user(hostname,msisdn):
            user= '****'
            password = '****'
            lh = '.****/users/reset'
            mn = '.****/users/reset'

            host  = hostname[:2]
            number = msisdn

            if  host  == 'lh':
                host = 'http://'+hostname+lh
                print (host)
            elif host  == 'md':
                host = 'http://'+hostname+mn
            else:
                print ('something wrong with host')

   
            request_headers = {'Content-Type': 'application/json'}
            
            print(host)
            #request = requests.delete(host, params={uuid: msisdn}, headers=request_headers,auth=(user,password))  
               
            
            


            #return request.content






a = SecureD.reset_user('****','****')
print(a)
