from inspect import stack, getframeinfo
from modules.util import storage
from datetime import datetime

DEBUG = True
D_ERROR = 0
D_INFO = 1
D_VERBOSE = 2
D_VOMIT = 3
D_CURRENT_LEVEL = 1

D_HEADER = ['ERROR', 'INFO', 'VERBOSE', 'VOMIT']


def on_ready():
    global D_CURRENT_LEVEL

    debug(D_INFO, 'Loading Debug module...')

    try:
        D_CURRENT_LEVEL = storage.load_bot_setting('debug_level')
    except KeyError as e:
        # Will I ever hit this?
        pass
    except EmptyFileException as e:
        storage.save_bot_setting('debug_level', D_CURRENT_LEVEL)

    debug(D_INFO, 'Debug ready.')


def debug(level, string):
    global D_CURRENT_LEVEL
    # _frame = inspect.currentframe()
    # caller = inspect.getframeinfo(_frame)[0]
    # caller = inspect.stack()[0]
    time = datetime.now().strftime('%H:%M:%S')
    caller = getframeinfo(stack()[1][0])
    name = caller.filename.split('\\')[-1].split('.')[0]
    line_number = caller.lineno
    if DEBUG:
        if level <= D_CURRENT_LEVEL:
            print('[{}][{}][{}][{}] {}'.format(time, name, line_number, D_HEADER[level], string))
    del caller


def on_exit():
    global D_CURRENT_LEVEL
    debug(D_INFO, 'Saving debug settings.')
    storage.save_bot_setting('debug_level', D_CURRENT_LEVEL)
    debug(D_INFO, 'Debug settings saved.')

