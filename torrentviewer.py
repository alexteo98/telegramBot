import math
import datetime
import logging
import qbt

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO,filename='/share/telegram-bot/telegrambot.log')
torrents=None

def view_torrents_detailed(torrent_ls):
    ''' 
    View detailed information of given torrent objects
    
    Parameters: 
    torrent_ls: List of Torrent objects

    Return:
    List<str> containing detailed information 
    corresponding to that torrent object
    '''
    
    info_ls=[]
    for torrent in torrent_ls:
        info_ls.append(detailed_torrent(torrent))
        
    return info_ls

def view_torrents_summary(torrent_ls):
    ''' 
    View summary information of given torrent objects
    Only contains name of torrent
    
    Parameters: 
    torrent_ls: List of Torrent objects

    Return:
    List<str> containing summary information 
    corresponding to that torrent object
    '''
    
    info_ls=[]
    for torrent in torrent_ls:
        info_ls.append(summary_torrent(torrent))
        
    return info_ls

def detailed_torrent(torrent):
    '''
    Returns the maximum details of a torrent
    Uses torrent_details function to get details
    
    Parameters:
    torrent: Torrent object to detail
    
    Return:
    Maximum information of torrent
    '''
    
    return torrent_details(torrent)
    
def summary_torrent(torrent):
    '''
    Returns the summary of a torrent
    Uses torrent_details function to get details
    Only retrieves name of torrent
    
    Parameters:
    torrent: Torrent object to detail
    
    Return:
    Summary of torrent
    '''
    
    return torrent_details(torrent,_ratio=False,_size=False,_seed_duration=False,_safe=False)

def torrent_details(torrent,_ratio=True,_size=True,_seed_duration=True,_safe=True):
    '''
    Returns the details of a torrent
    
    Parameters:
    torrent: Torrent object to detail
    _ratio -> bool: Specifies to get ratio information or not
    _size -> bool: Specifies to get size information or not
    _seed_duration -> bool: Specifies to get seeded duration or not
    _safe -> bool: Specifies to see if safe to remove or not
    
    Return:
    The details of the given torrent based on the amount of information specified
    
    Example:
    Jirisan.S01E08.1080p.WEB-DL.H264.AAC-AppleTor.mp4
    Ratio: 2.14
    Size: 2.32
    Seeded Duration: 34 days, 12:09:31
    Safe to Remove
    '''
    
    s=''
    name_str=''
    ratio_str=''
    size_str=''
    seed_duration_str=''
    safe_str=''
    
    try:
        name_str=torrent.name + '\n'
        ratio=math.floor(torrent.ratio*100)/100
        size=torrent_size(torrent)
        seed_duration=datetime.timedelta(seconds=torrent.seeding_time)
        safe=check(torrent)
    except:
        logging.warning('Failed to fetch torrent details!')
        return s
        
    if _ratio:
        ratio_str='Ratio: ' + str(ratio) + '\n'
    if _size:
        size_str= 'Size: ' + str(size) + '\n'
    if _seed_duration:
        seed_duration_str='Seeded Duration: ' + str(seed_duration) + '\n'
    if _safe:
        if safe:
            safe_str='Safe to Remove' + '\n'
        else:
            safe_str='Seeding time not reached' + '\n'
    
    s= str(name_str)+str(ratio_str)+str(size_str)+str(seed_duration_str)+str(safe_str)

    return s

def get_downloading_torrents():
    torrent_ls=qbt.get_torrents(status='downloading')
    return torrent_ls

def get_safe_remove_torrents():
    torrent_ls_raw=qbt.get_torrents()
    torrent_ls=[]
    for torrent in torrent_ls_raw:
        if check(torrent):
            torrent_ls.append(torrent)
    
    return torrent_ls

def get_all_torrents():
    return qbt.get_torrents()

def check(torrent):
    if (torrent.ratio > 1.05):
        return True

    size=torrent_size(torrent)
    time=torrent_seed_time(torrent)
    if (seed_time_req(torrent)<time):
        return True
    return False

def torrent_size(torrent):
    size=torrent.size/1073741824
    size*=100
    size=math.ceil(size)
    return size/100

def seed_time_req(torrent):
    size=torrent_size(torrent)
    if (size <= 5):
        time = 72
    elif (size < 50):
        time = 72+(2*size)
    else:
        time = 100*math.log(size)-219.2023

    time *= 1.05
    return time

def torrent_seed_time(torrent):
    return torrent.seeding_time/3600

def test():
    '''Test doc'''
    details=view_torrents_summary(get_all_torrents())
    for detail in details:
        print(detail)

def main():
    #print(view_torrents_detailed.__doc__)
    #print(qbt.get_torrents()[0])
    #print(view_torrents_detailed(qbt.get_torrents())[0])
    test()
    
if __name__ == '__main__':
    main()
