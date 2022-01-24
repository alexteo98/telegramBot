import responses
from telegram.ext import *
import logging
import os
import requests
import json

# setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO,filename='/share/telegram-bot/telegrambot.log')

logging.info('Starting Bot...')
API_KEY=os.getenv('TELEGRAM_BOT_API_KEY')
ALLOWED_USERS=[os.getenv]

#global variables
updater=None

def handle_message(update, context):
    if not check_allowed_update(update):
        return unauth(update)
    else:
        text=str(update.message.text).lower()
        logging.info(f'User ({update.message.chat.id}) says: {text}')
        response = responses.get_response(text)
        for txt in response:
            update.message.reply_text(txt)

def handle_file(update,context):
    if not check_allowed_update(update):
        return unauth(update)
    else:
        file_id=update.message['document']['file_id']
        logging.info(file_id)
        download_file(file_id)

def download_file(file_id):
    filepath=get_file_path(file_id)
    download_file_to_fs(filepath)

def get_file_path(file_id)->str:
    url='https://api.telegram.org/bot' + API_KEY + '/getFile?file_id=' + file_id
    logging.info(url)

    r=requests.get(url)
    j=r.json()
    file_path=j['result']['file_path']
    return file_path

def download_file_to_fs(file_path):
    DL_LOCATION='/share/samsung/Torrents/'
    url='https://api.telegram.org/file/bot' + API_KEY + '/' + file_path
    name=file_path.split('/')[1]
    full_path=DL_LOCATION+name

    r=requests.get(url)
    open(full_path,'wb').write(r.content)

def start_command(update, context):
    if not check_allowed_update(update):
        return unauth(update)
    else:
        update.message.reply_text("start")
    pass

def end_command(update, context):
    if not check_allowed_update(update):
        return unauth(update)
    else:
        update.message.reply_text("end")
    pass

def unauth(update):
    chat_id=update.message.chat.id
    name=str(update.message.from_user.first_name)+' '+str(update.message.from_user.last_name)
    update.message.reply_text('Access Denied!')
    notify='Unauthorised bot access from chat ID: '+str(chat_id)+', name: '+ name
    updater.bot.sendMessage(chat_id=120049794,text=notify)
    logging.warning('Unauthorized user from chat ID: '+ str(chat_id)+', name: '+name)
    

def check_allowed_update(update):
    chat_id=update.message.chat.id
    if chat_id in ALLOWED_USERS:
        return True
    return False

def error(update, context):
    logging.error(f'Update {update} caused error {context.error}')

def main():
    global updater
    updater = Updater(API_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('end', end_command))
    #dp.add_handler(CommandHandler('help', help_command))
    
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_handler(MessageHandler(Filters.document, handle_file))
    dp.add_error_handler(error)

    updater.start_polling(1.0)
    updater.idle()

if __name__ == '__main__':
    main()
