'''
all functions that do some kind of logging
'''

import datetime as dt


def error_logging(file):
    import logging
    logging.basicConfig(
        filename=file,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
    logging.info('Will now attempt to start up the bot...')


def chat_id_logging(update, context):
    logfile = 'request_logs/{}_{}.log'.format(
        dt.date.today(),
        update.effective_chat.id # maybe there is some smarter identifier to store
    )
    logtext = update.message.text + '\n'
    with open(logfile, 'a') as f:
        f.write(logtext)