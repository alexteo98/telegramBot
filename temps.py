import math
import os
import subprocess as sp
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO,filename='/share/telegram-bot/telegrambot.log')

query_result=''
query_result_error=''
query_result_cpu=''
query_result_error_cpu=''
process_hdd=None
process_cpu=None

_drive_names=  { 
        '3tb' : 'ST3000VX009-2AY10G',
        '4tb' : 'WDC WD40EFAX-68JH4N',
        'samsung 1tb' : 'Samsung M3 Portable',
        'kingston ssd' : 'KINGSTON RBU-SC100S37240EG'
        }

_dict= { 
        '3tb' : 'Uninitialized', 
        '4tb' : 'Uninitialized', 
        'cpu' : 'Uninitialized', 
        'mobo': 'Uninitialized'
        }

def call_ext():
    global process_hdd
    global process_cpu
    global query_result
    global query_result_cpu
    try:
        process_hdd=sp.run(['/share/bot/temps'], capture_output=True)
        logging.info('HDD Temperatures retrieved')
    except:
        logging.error('Error Retrieving HDD Temperatures!')
        query_result=''
        query_result_error=''
    else:
        query_result=str(process_hdd.stdout, errors='ignore').rstrip('\n')
        query_result_error=str(process_hdd.stderr, errors='ignore').rstrip('\n')

    try:
        process_cpu=sp.run(['/share/bot/cpu_temps'], capture_output=True, text=True)
        logging.info('CPU Temperatures retrieved')
    except:
        logging.error('Error Retrieving CPU Temperatures!')
        query_result_cpu=''
        query_result_error_cpu=''
    else:
        query_result_cpu=process_cpu.stdout.rstrip('\n')
        query_result_error_cpu=process_cpu.stderr.rstrip('\n')


def update_results():
    call_ext()    

    update_3tb_temp()
    update_4tb_temp()
    update_cpu_temp()
    update_mobo_temp()

    return

def update_3tb_temp():
    global _dict
    global query_result
    global query_result_error
    name=_drive_names['3tb']
    
    if name in  query_result:
        temp=query_result
        temp=temp.split('\n')
        try:
            for string in temp:
                if name in string:
                    result=string.split(':')[2][1:3]
                    _dict['3tb']=int(result)
                    return
        except:
            _dict['3tb']='Error'
            logging.error('Failed to fetch 3TB HDD Temperature!')
            logging.debug('Failed to parse result!')
        else:
            _dict['3tb']='Error'

    else:
        _dict['3tb']='Error'
        logging.error('Failed to fetch 3TB HDD Temperature!')

def update_4tb_temp():
    global _dict
    global query_result
    global query_result_error
    name=_drive_names['4tb']
    
    if name in  query_result:
        temp=query_result
        temp=temp.split('\n')
        try:
            for string in temp:
                if name in string:
                    result=string.split(':')[2][1:3]
                    _dict['4tb']=int(result)
                    return
        except:
            _dict['4tb']='Error'
            logging.error('Failed to fetch 3TB HDD Temperature!')
            logging.debug('Failed to parse result!')
        else:
            _dict['4tb']='Error'

    else:
        _dict['4tb']='Error'
        logging.error('Failed to fetch 4TB HDD Temperature!')

def update_cpu_temp():
    global _dict
    global query_result_cpu
    global query_result_error_cpu
    try:
        s=query_result_cpu.split('\n')[1]
        deg=int(s)
        deg=math.ceil(deg/1000)
        _dict['cpu']=deg
    except:
        _dict['cpu']='Error'
        logging.error('Failed to fetch CPU Temperature!')

def update_mobo_temp():
    global _dict
    global query_result_cpu
    global query_result_error_cpu
    try:
        s=query_result_cpu.split('\n')[0]
        deg=int(s)
        deg=math.ceil(deg/1000)
        _dict['mobo']=deg
    except:
        _dict['mobo']='Error'
        logging.error('Failed to fetch Mobo Temperature!')

def get_temps():
    message=[]
    update_results()
    #cputemps=get_cpu_temps()
    #hddtemps=get_hdd_temps()
    s=      'Current Temperatures:\n' +\
            'Motherboard: ' + str(_dict['mobo']) + '\n'\
            'CPU Core: ' + str(_dict['cpu']) + '\n'\
            '4TB HDD: ' + str(_dict['4tb']) + '\n'\
            '3TB HDD: ' + str(_dict['3tb']) 

    message.append(s)
    return message

if __name__  == '__main__':
    print(get_temps()[0])
