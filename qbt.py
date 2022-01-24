import math
import datetime
import qbittorrentapi
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO,filename='/share/telegram-bot/telegrambot.log')

client = qbittorrentapi.Client(host='192.168.1.100', port=9090, username='alexteo98', password='alexteo98')

try:
    client.auth_log_in()
except qbittorrentapi.LoginFailed as e:
    print(e);


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

def tag_safe(torrent):
    client.torrents_add_tags(tags='remove', torrent_hashes=torrent.hash)

def get_torrents_list(status=True, ratio=True, size=True, seed_duration=True, safe=True):
    ls=[]
    
    for torrent in client.torrents_info():
        text=torrent.name
        
        if ratio:
            text+=("\nRatio: " + str(math.floor(torrent.ratio*100)/100))
        if size:
            text+=("\nSize: " + str(torrent_size(torrent))+str(' GB'))
        if seed_duration:
            text+=("\nSeeded Duration: " + str(datetime.timedelta(seconds=torrent.seeding_time)))
        if safe:
            if check(torrent):
                text+=("\nsafe to remove")
                #tag_safe(torrent)
            else:
                text+=("\nnot ok")
                text+=("\nTime left: " + str(seed_time_req(torrent)-torrent_seed_time(torrent)))
        text+='\n'
        ls.append(text)
        #break

    return ls

def get_torrents(status='all'):
    return client.torrents_info(status_filter=status)

def delete_torrent(torrent_hash):
    client.torrents_delete(torrent_hashes=torrent_hash)

def resume_torrent(torrent_hash):
    client.torrents_resume(torrent_hashes=torrent_hash)

def pause_torrent(torrent_hash):
    client.torrents_pause(torrent_hashes=torrent_hash)

def main():
    for torrent in client.torrents_info():
        if check(torrent):
            tag_safe(torrent)
            print('Tagged safe' + torrent.name)
        
if __name__ == '__main__':
    main()
