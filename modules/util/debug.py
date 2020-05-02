import inspect
from modules.util import storage
from datetime import datetime

DEBUG = True
D_ERROR = 0
D_INFO = 1
D_VERBOSE = 2
D_VOMIT = 3
D_CURRENT_LEVEL = 2

D_HEADER = ['ERROR', 'INFO', 'VERBOSE', 'VOMIT']


def on_ready():
    try:
        debug.D_CURRENT_LEVEL = storage.load_server_setting('debug_level')
    except KeyError as e:
        pass


def debug(level, string):
    global D_CURRENT_LEVEL
    # _frame = inspect.currentframe()
    # caller = inspect.getframeinfo(_frame)[0]
    # caller = inspect.stack()[0]
    time = datetime.now().strftime('%H:%M:%S')
    if DEBUG:
        if level <= D_CURRENT_LEVEL:
            print('[{}][{}] {}'.format(time, D_HEADER[level], string))
    # del _frame


def on_exit():
    global D_CURRENT_LEVEL
    storage.save_server_setting('debug_level', D_CURRENT_LEVEL)

