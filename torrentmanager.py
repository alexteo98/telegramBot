import qbt
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO,filename='/share/telegram-bot/telegrambot.log')

def resume_torrent(torrent_hash):
    qbt.resume_torrent(torrent_hash)

def pause_torrent(torrent_hash):
    qbt.pause_torrent(torrent_hash)

def delete_torrent(torrent_hash):
    qbt.delete_torrent(torrent_hash)
    pass

def upload_torrent_file():
    pass

def main():
    pass

if __name__ == '__main__':
    main()
