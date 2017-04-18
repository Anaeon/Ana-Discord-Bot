import shelve
import pprint

class StorageException(Exception):
	"""base class for Storage exceptions"""
	pass

class NoSuchAttributeException(StorageException):
	"""exception raised when an attribute doesn't exist"""
	pass

def get_user_info(id):
	with shelve.open('data/user') as s:
		existing = s[id]
	return existing

def get_user_attribute(id, key):
	existing = get_user_info(id)

	return existing[key]

def set_user_attribute(id, key, value):
	with shelve.open('data/user', writeback=True) as s:
		if not id in s:
			s[id] = {}
		s[id][key] = value

def remove_user_attribute(id, key):
	with shelve.open('data/user', writeback=True) as s:
		del s[id][key]

def get_attribute_for_users(key):
	user_list = []
	with shelve.open('data/user') as s:
		for id in s:
			try:
				user_list.append({"id": id, key: s[id][key]})
			except KeyError as e:
				pass

	return user_list

def get_server_info(id):
	with shelve.open('data/server') as s:
		existing = s[id]
	return existing

def get_server_attribute(id, key):
	existing = get_server_info(id)
	
	return existing[key]
	
def set_server_attribute(id, key, value):
	with shelve.open('data/server', writeback=True) as s:
		if not id in s:
			s[id] = {}
		s[id][key] = value
		
def remove_server_attribute(id, key):
	with shelve.open('data/server', writeback=True) as s:
		del s[id][key]
		
def get_attribute_for_servers(key):
	server_list = []
	with shelve.open('data/server') as s:
		for id in s:
			try:
				server_list.append({"id": id, key: s[id][key]})
			except KeyError as e:
				pass
	return server_list