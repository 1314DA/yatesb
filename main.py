'''
this is Yet Another TElegram Stock Bot (YATESB)
it helps me to keep up to date with my stocks
based on the yfinance module by Ran Aroussi
'''

#---------- general module imports ----------#
import sys
import datetime as dt
from os import path, mkdir
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters


#---------- define functions ----------#
import func_basic as fb
import func_yfinance_interaction as fyf
import func_logging as fl


#---------- get token ----------#
with open('../telegram_bot_token', 'r') as f:
    token = f.readline().strip()


#---------- create handlers from functions ----------#
log_request_by_chat_id_handler = MessageHandler(
    Filters.text,
    fl.chat_id_logging,
    pass_user_data=True,
    pass_chat_data=True,
) # directory for logs is defined in 'func_logging.py'
start_handler = CommandHandler('start', fb.start)
unknown_handler = MessageHandler(Filters.text, fb.unknown)
help_handler = CommandHandler('help', fb.help)
stck_business_summary = CommandHandler('business', fyf.print_business_summary)
stck_daily_vaules = CommandHandler('daily', fyf.print_daily_values)
stck_plt_hist_dividend = CommandHandler('dividend', fyf.print_plot_dividends)
stck_plt_hist_value = CommandHandler('history', fyf.print_plot_historical)
stck_website_handler = CommandHandler('website', fyf.print_website)


#---------- define main procedure ----------#
def main(token):

    # logging directories and files
    if not path.isdir('error_logs'):
        mkdir('error_logs')

    if not path.isdir('request_logs'):
        mkdir('request_logs')
    fl.error_logging('error_logs/{}.log'.format(dt.date.today()))

    if not path.isdir('user_watchlists'):
        mkdir('user_watchlists')

    # initialize the bot
    updater = Updater(
        token=token,
        use_context=True
    )
    dispatcher = updater.dispatcher

    # add logging handlers
    dispatcher.add_handler(log_request_by_chat_id_handler, group=1)

    # add functionality handlers to dispatcher
    dispatcher.add_handler(start_handler)

    dispatcher.add_handler(stck_business_summary)
    dispatcher.add_handler(stck_daily_vaules)
    dispatcher.add_handler(stck_plt_hist_dividend)
    dispatcher.add_handler(stck_plt_hist_value)
    dispatcher.add_handler(stck_website_handler)
    
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(unknown_handler) # this must always be handeled last
    
    # add error handlers
    dispatcher.add_error_handler(fyf.print_err)


    # start up bot and keep idle until interrupt
    print('starting telegram bot...')
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main(token)
