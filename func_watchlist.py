'''
allow to create a personal watchlist with up to 6 elements
function for adding an item to the watchlist
function for removing an item from watchlist
interactive buttons for each watchlist item
interactively chose what to do with watchlist item
'''


from os import path


class Watchlist:
    def __init__(self, user_id):
        self.watchlistfile = 'user_watchlists/watchlist_{}.txt'.format(user_id)
        self.symbols = []

    def check_user_watchlist(self):
        try:
            if path.isfile(self.watchlistfile):
                with open self.watchlistfile as wf:
                    self.symbols.append(wl.readline())
            else:
                open(self.watchlistfile, 'a').close()
        except:
            raise RuntimeError('could not access or create watchlist')

    def add_item(self, symbol):
        if len(self.symbols) < 6:
            self.symbols.append(symbol)
        elif len(self.symbols) >= 6:
            raise RuntimeError('watchlist contains max. number of elements')

    def remove_item(self, symbol):
        pass

    def save_watchlist(self):
        pass

