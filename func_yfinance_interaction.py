''' wrapper functions for interacting with yfinance
'''

import yfinance as yf
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import datetime
from expiringdict import ExpiringDict


# create cache inside memory in order to speed up getting stock information
# --> cache on hard drive in the future?
cached_stocks = ExpiringDict(
    max_len = 100,
    max_age_seconds = 3600
)


#---------- functions loading stuff from online ----------#

def get_all_stock_data(symbol, cache=cached_stocks):
    '''
    get all available data for given symbol
    preferentially used cached data from the last hour
    if no cached data available try to get data from yfinance

    Parameters
    ----------
    symbol : str
        stock symbol of yahoo finanace
    cache : dict, ExpiringDict
        dictionary that holds cached stock data
        dict contains 'symbol':'yfinance.Ticker object'

    Raises
    ------
    NameError
        if no info data found for symbol

    Returns
    -------
    stock : yfinance.Ticker object
        contains all yahoo finance data on the given stock

    '''

    try: # to read stored stock data
        stock = cached_stocks.get(symbol)
        stock.info
    except: # read stock data from internet
        stock = yf.Ticker(symbol)
        try: # check if stock contains something, if True cache data
            stock.info
            cached_stocks[symbol] = stock
        except:
            raise NameError('no data for stock symbol found')
 
    return stock


#---------- filter functions use yfinance.Ticker objects as input ----------#

def filter_business_summary(stock):
    '''
    filter information on stock business

    Parameters
    ----------
    stock : yfinance.Ticker
        stock obtained with yfinance.Ticker method

    Raises
    ------
    KeyError
        if no data found in stock.info

    Returns
    -------
    business_summary : str
        summary of information on stock business

    '''
    
    try:
        business_summary = stock.info['longBusinessSummary']
    except:
        raise KeyError('specified data for stock symbol not found')
    
    return business_summary


def filter_currency(stock):
    '''
    filter stock website

    Parameters
    ----------
    stock : yfinance.Ticker
        stock obtained with yfinance.Ticker method

    Returns
    -------
    currency : str
        currency name or 'n/a' if not available

    '''
    
    try:
        currency = stock.info['currency']
    except:
        currency = 'n/a'
    
    return currency


def filter_daily_values(stock):
    '''
    filter information on today's stock values
    NOTE: still think of a nicer way to present this infomation
        (maybe graphically)

    Parameters
    ----------
    stock : yfinance.Ticker
        stock obtained with yfinance.Ticker method

    Raises
    ------
    KeyError
        if no data found in stock.info

    Returns
    -------
    daily : str
        summary of today's stock evolution

    '''
    
    currency = filter_currency(stock)
    
    try:
        regularMarketPreviousClose = stock.info['regularMarketPreviousClose']
        regularMarketOpen = stock.info['regularMarketOpen']
        regularMarketDayLow = stock.info['regularMarketDayLow']
        regularMarketDayHigh = stock.info['regularMarketDayHigh']
        ask = stock.info['ask']
        bid = stock.info['bid']
    except:
        raise KeyError('specified data for stock symbol not found')
        
    daily = ('close yesterday: {} {}\n'.format(regularMarketPreviousClose, currency) +
             'open today: {} {}\n'.format(regularMarketOpen, currency) +
             'low today: {} {}\n'.format(regularMarketDayLow, currency) +
             'high today: {} {}\n'.format(regularMarketDayHigh, currency) +
             'bid / ask: {} {} / {} {}'.format(bid, currency, ask, currency) )
    
    return daily


def filter_website_url(stock):
    '''
    filter stock website

    Parameters
    ----------
    stock : yfinance.Ticker
        stock obtained with yfinance.Ticker method

    Raises
    ------
    KeyError
        if no data found in stock.info

    Returns
    -------
    url : str
        url of stock

    '''
    
    try:
        url = stock.info['website']
    except:
        raise KeyError('specified data for stock symbol not found')
    
    return url


#---------- plot functions make a pyplot ----------#

def plot_n_day_historical_value(stock, n):
    '''
    plot the historical data (at close) of the last n working days

    Parameters
    ----------
    stock : yfinance.Ticker
        stock obtained with yfinance.Ticker method
    n : int
        number of working days to include in plot

    Returns
    -------
    retval : int
        = 0 if everything worked fine
        = 1 if no historical data could be found
        = 2 if historical data found but plotting not possible
        
    Yields
    -------
    tmp.png : image file
        stock data for n days to the past in a pyplot graph stored as png
    '''
    
    retval = 0

    try:
        hist = stock.history(period='max')[-int(n):-1] # is a pandas DataFrame
        currency = filter_currency(stock)
    except:
        retval = 1

    if retval == 0:
        try:
            fig = plt.figure(figsize=(6,4))
            ax = fig.add_subplot(111)
            ax.set_xlabel('date')
            ax.set_ylabel('absolute value in {}'.format(currency))
            ax.plot(hist.index, hist['Close'])
            plt.savefig('tmp.png')
        except:
            retval = 2

    return retval


def plot_historical_dividends(stock):
    '''
    plot the historical dividends

    Parameters
    ----------
    stock : yfinance.Ticker
        stock obtained with yfinance.Ticker method

    Returns
    -------
    retval : int
        = 0 if everything worked fine
        = 1 if no historical data could be found
        = 2 if historical data found but plotting not possible
    dividend_latest : float
        latest dividend
        
    Yields
    -------
    tmp.png : image file
        dividends over time in a pyplot graph stored as png
    '''
    
    retval = 0

    try:
        dividends = stock.dividends
        dividend_latest = stock.info['dividendRate']
        currency = filter_currency(stock)
    except:
        retval = 1

    if retval == 0:
        try:
            fig = plt.figure(figsize=(6,4))
            ax = fig.add_subplot(111)
            ax.set_xlabel('date')
            ax.set_ylabel('dividend value in {}'.format(currency))
            ax.plot(dividends.index, dividends)
            plt.savefig('tmp.png')
        except:
            retval = 2
    
    return retval, dividend_latest


#---------- print functions give stuff to telegram chat ----------#

def print_business_summary(update, context):
    '''
    send stock business summary to chat

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
        returns string with stock business summary
    '''

    symbol = context.args[0]
    stock = get_all_stock_data(symbol)
    summary = filter_business_summary(stock)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=summary
    )


def print_daily_values(update, context):
    '''
    send today's stock values to chat

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
        returns string with today's stock values
        ATTENTION: may be up to one hour old (see cache above)
    '''

    symbol = context.args[0]
    stock = get_all_stock_data(symbol)
    daily_vaules = filter_daily_values(stock)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=daily_vaules
    )


def print_website(update, context):
    '''
    send stock company website to chat

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
        returns string with stock company website
    '''

    symbol = context.args[0]
    stock = get_all_stock_data(symbol)
    url = filter_website_url(stock)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=url
    )


def print_plot_historical(update, context):
    '''
    send historical stock closing value to chat

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
        returns image with historical stock closing value
    '''

    symbol = context.args[0]
    # add option to specify the days to plot
    n=100
    stock = get_all_stock_data(symbol)
    fig = plot_n_day_historical_value(stock, n)
    
    if fig == 0:
        with open('tmp.png', 'rb') as img:
            context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=img,
            caption='Closing values of the last {} days'.format(n)
            )
    else:
        context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='ERROR: code {}'.format(fig)
        )


def print_plot_dividends(update, context):
    '''
    send historical dividends to chat

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
        returns image with historical stock closing value
    '''

    symbol = context.args[0]
    stock = get_all_stock_data(symbol)
    val, rate = plot_historical_dividends(stock)
    
    if val == 0:
        with open('tmp.png', 'rb') as img:
            context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=img,
            caption='Latest dividend was {}'.format(rate)
            )
    else:
        context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='ERROR: code {}'.format(val)
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
    except NameError as err:
        context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='ERROR: {}'.format(err)
        )
    except KeyError as err:
        context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='ERROR: {}'.format(err)
        )
    except IndexError:
        context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='ERROR: you are possibly missing an argument for this command'
        )