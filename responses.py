import qbt
import ping
import logging
import temps

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO,filename='/share/telegram-bot/telegrambot.log')
states_dict={}

def populate_dict():
    global states_dict
    states_dict={  
            'error':'Errored', 
            'missingFiles' : 'Missing Data Files' ,
            'uploading' : 'Completed - Uploading' ,
            'pausedUP' : 'Completed - Paused' ,
            'queuedUP' : 'Completed - Queued' ,
            'stalledUP' : 'Completed - Stalled' ,
            'checkingUP' : 'Completed - Checking' ,
            'forcedUP' : 'Forced Uploading' ,
            'allocating' : 'Allocating Disk Space' ,
            'downloading' : 'Incomplete - Downloading' ,
            'metaDL' : 'Fetching Metedata' ,
            'pausedDL' : 'Incomplete - Paused' ,
            'queuedDL' : 'Incomplete - Queued' ,
            'stalledDL' : 'Incomplete - Stalled' ,
            'checkingDL' : 'Incomplete - Checking' ,
            'forcedDL' : 'Forced Downloading' ,
            'checkingResumeData' : 'Checking' ,
            'moving' : 'Moving' ,
            'unknown' : 'Unknown'   }

# get_response takes in the message sent by the user and returns the message to be sent back
def get_response(text):
    s=''
    ls=text.split(' ')
    if ls[0] == 'ping':
        s=ping.handle_request(ls[1])
                
    elif ls[0] == 'view':
        #logging.info('view')
        if ls[1] == 'detailed':
            # view detailed info
            logging.info('Gettting detailed torrent list')
            s=get_all_torrents_list_full_details()
        elif ls[1] == 'summary':
            # view short summary
            logging.info('Gettting torrent summary')
            s=get_all_torrents_list_simple()
            
        s=number_torrents(s)
        s=format_message(s)
        s=number_pages(s)
    
    elif ls[0] == 'temperatures' or ls[0] == 'temperature':
        logging.info('Getting temperatures')
        s=temps.get_temps()

    else:
        s=['Invalid input!']
    return s

def get_all_torrents_list_full_details():
#    s=qbt.get_torrents_list()
    return qbt.get_torrents_list()

def get_all_torrents_list_simple():
    # torrents only name and status
#    s=qbt.get_torrents_list(size=False, ratio=False, seed_duration=False, safe=False)
#    for i in range(len(s)):
#        s[i]=str(s)+': '+s[i]
    return qbt.get_torrents_list(size=False, ratio=False, seed_duration=False, safe=False)


def format_message(ls):
    new_ls=[]
    s=''
    i=0
    c=0
    while(i!=len(ls)):
        length1=len(s)
        length2=len(ls[i])
        if ((length1+length2)>4000):
            # split message
            new_ls.append(s)
            s=''
        else:
            s+=ls[i]
            s+='\n'
            i+=1

    new_ls.append(s)

    return new_ls

def number_torrents(ls):
    for i in range(len(ls)):
        ls[i]=str(i+1)+' --- '+ls[i]

    return ls

def number_pages(ls):
    if len(ls)==1:
        return ls
    else:
        for i in range(len(ls)):
            ls[i]='Page '+str(i+1)+':\n'+ls[i]

    return ls
