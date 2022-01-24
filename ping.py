#from typing import List
import subprocess as sp
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO,filename='/share/telegram-bot/telegrambot.log')

global known_hosts
known_hosts={  
        'gateway': [192,168,1,254], 
        'desktop' : [192,168,1,37] ,
        'rpi0' : [192,168,1,35] ,
        'printer' : [192,168,1,1] ,
        'server' : [192,168,1,100]
        }

def main():
    #result=ping_host_ip([192, 168, 1, 254])
    #ping_host_hostname('google.com')
    #print(result)
    pass

def handle_request(text):
    
    if text in known_hosts:
        ls=known_hosts[text]
        byte0=int(ls[0])
        byte1=int(ls[1])
        byte2=int(ls[2])
        byte3=int(ls[3])
        hostname=str(byte0)+'.'+str(byte1)+'.'+str(byte2)+'.'+str(byte3)
        return [ping_host(hostname)]
    
    if is_hostname(text):
        # Disabled Feature
        # return [ping_host(text)]
        pass
        
    if is_ip_address(text):
        ls=text.split('.')
        byte0=int(ls[0])
        byte1=int(ls[1])
        byte2=int(ls[2])
        byte3=int(ls[3])
        hostname=str(byte0)+'.'+str(byte1)+'.'+str(byte2)+'.'+str(byte3)
        return [ping_host(hostname)]
        
    return ['Invalid Host!']

def is_hostname(text)->bool:
    # Disabled feature
    return False
    
def is_ip_address(text)->bool:
    ls=text.split('.')
    
    if (len(ls)!=4):
        logging.info('Invalid IP entered: ' + str(text))
        return False
    else:
        byte0=ls[0]
        byte1=ls[1]
        byte2=ls[2]
        byte3=ls[3]
        if (convertible_to_int(byte0) and convertible_to_int(byte1) and convertible_to_int(byte2) and convertible_to_int(byte3)):
            # all are integers, check values between 0-254 next
            byte0=int(byte0)
            byte1=int(byte1)
            byte2=int(byte2)
            byte3=int(byte3)
            
            #check byte values
            if (byte0 < 0 or byte0 > 254):
                logging.info('Invalid IP entered(First octet): ' + str(text))
                return False
            
            if (byte1 < 0 or byte1 > 254):
                logging.info('Invalid IP entered(Second octet): ' + str(text))
                return False
                
            if (byte2 < 0 or byte2 > 254):
                logging.info('Invalid IP entered(Third octet): ' + str(text))
                return False
                
            if (byte3 < 0 or byte3 > 254):
                logging.info('Invalid IP entered(Fourth octet): ' + str(text))
                return False

            return True          
            
    return False

def request(text):
    result=[]
    
    ping_result=''
    error=False
    ls=text.split('.')
    if (len(ls)!=4):
        error=True
    else:
        byte0=ls[0]
        byte1=ls[1]
        byte2=ls[2]
        byte3=ls[3]
        if (convertible_to_int(byte0) and convertible_to_int(byte1) and convertible_to_int(byte2) and convertible_to_int(byte3)):
            # all are integers, check values between 0-254 next
            byte0=int(byte0)
            byte1=int(byte1)
            byte2=int(byte2)
            byte3=int(byte3)
            
            #check byte values
            if (byte0 < 0 or byte0 > 254):
                logging.info('Invalid IP entered(First octet): ' + str(text))
                error=True
            
            if (byte1 < 0 or byte1 > 254):
                logging.info('Invalid IP entered(Second octet): ' + str(text))
                error=True
                
            if (byte2 < 0 or byte2 > 254):
                logging.info('Invalid IP entered(Third octet): ' + str(text))
                error=True
                
            if (byte3 < 0 or byte3 > 254):
                logging.info('Invalid IP entered(Fourth octet): ' + str(text))
                error=True
            
            if not error:
                ping_result=ping_host_ip([byte0,byte1,byte2,byte3])            
            
        else:
            error=True
    
    if not error:
        result.append(ping_result)
    else:
        result.append('Invalid Hostname!')

    return result

def ping_host_ip(host_ls) -> str:
    # input given in length 4  list,  each corresponding to each byte

    hostname=str(host_ls[0])+'.'+str(host_ls[1])+'.'+str(host_ls[2])+'.'+str(host_ls[3])
    ping_command='ping -c2 -w2 ' + hostname
    logging.info('Pinging '+hostname)
    result=sp.run(ping_command, shell='/bin/sh', stdout=sp.PIPE)
    success = result.returncode
    if success==0:
        logging.info(hostname+' is up')
        return(hostname+' is up!')
    logging.info(hostname+' is down')
    return(hostname+' is down!')

def ping_host(host) -> bool:
    # input given as hostname

    hostname=host
    ping_command='ping -c2 -w2 ' + hostname
    result=sp.run(ping_command, shell='/bin/sh', stdout=sp.PIPE)
    success = result.returncode
    if success==0:
        logging.info(hostname+' is up')
        return(hostname+' is up!')
    logging.info(hostname+' is down')
    return(hostname+' is down!')

def convertible_to_int(text:str)->bool:
    try:
        int(text)
        return True
    except ValueError:
        return False
    except:
        logging.debug('Exception during convertible_to_int check')
        return False






if __name__ =='__main__':
    main()
