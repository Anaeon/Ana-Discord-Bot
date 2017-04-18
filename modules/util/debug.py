DEBUG = True
D_ERROR = 0
D_INFO = 1
D_VERBOSE = 2
D_CURRENT_LEVEL = 1

D_HEADER = ['ERROR', 'INFO', 'VERBOSE']

def debug(l, s):
	if DEBUG:
		if l <= D_CURRENT_LEVEL:
			print('[{}] {}'.format(D_HEADER[l], s))