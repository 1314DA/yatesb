'''
basic text fuctions e.g. for using
start, help, etc.
'''


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='I would like to become your personal stock info bot.'
    )


def unknown(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='You did send a message I could not understand: "{}"'.format(
            update.message.text)
    )

# is there a way to automatically get all added handlers from the dispatcher?
def help(update, context):
    all_commands = [
        '/help - display this help',
        '/start - welcome message',
        '/business <symbol> - business summary',
        "/daily <symbol> - today's stock data",
        '/website <symbol> - stock/business website',
        '/history <symbol> - last 100 day stock records',
        '/dividend <symbol> - most recent dividends'
    ]
    help_text = '\n'.join(all_commands)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=help_text
    )


#---------- error handler functions ----------#

def print_err(update, context):
    '''
    send error message for stock data functions to chat

    Parameters
    ----------
    update : telegram.ext.Updater
        hands over the update from telegram chat
    context : telegram.ext.CallbackContext
        context for dispatcher

    Raises
    ------
    for errors see 'print_err' below

    Returns
    -------
    context.bot.send_message : telegram.ext.CallbackContext method
        return message to effective chat id
        returns string with error message for stock data functions
    '''

    try:
        raise context.error
    except IndexError:
        context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='ERROR: you are possibly missing an argument for this command'
        )
    except RuntimeError as err:
        context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='ERROR: {}'.format(err)
        )    