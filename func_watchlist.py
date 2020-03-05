'''
allow to create a personal watchlist with up to 6 elements
function for adding an item to the watchlist
function for removing an item from watchlist
interactive buttons for each watchlist item
interactively chose what to do with watchlist item
'''

from os import path

def create_user_watchlist(user_id):
    watchlistfile = 'user_watchlists/watchlist_{}.txt'.format(user_id)
    if not path.isfile(watchlistfile):
        open(watchlistfile, 'a').close()


def add_item_to_watchlist(symbol):
    pass