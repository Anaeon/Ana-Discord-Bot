import logging
import os
# import shelve
import json
import datetime

from pathlib import Path
from modules.data import misc

frmt = logging.Formatter(misc.LOGGER_FORMATTING)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
c_out = logging.StreamHandler()
c_out.setFormatter(frmt)
log.addHandler(c_out)

# TODO: Clean this file for fuck's sake... unneeded methods and unneeded code.
# TODO: Refactor all shadows to built-in "file" to be "f".
# TODO: Refactor all shadows...


class StorageException(Exception):
    """base class for Storage exceptions"""
    pass


class NoSuchAttributeException(StorageException):
    """exception raised when an attribute doesn't exist"""
    pass

class NoSuchSettingException(StorageException):
    """Exception raised when the requested setting doesn't exist inside the JSON file."""
    pass

def dump(json_object : json, target_file) -> json:
    json.dump(json_object, target_file, indent=4, sort_keys=True)


def on_ready(client):
    # TODO: Make sure all the appropriate files have been generated here beforehand.

    # Bot settings.
    Path('data/settings.json').touch(exist_ok=True) # If the file is not, make it so.
    if os.path.getsize('data/settings.json') < 1: # If the file has no data...
        # Make some new data.
        new_data = {
            "debug_level" : 0
        }
        # Dump it in the file.
        with open('data/settings.json', 'w') as f:
            dump(new_data, f)

    # Server settings.
    for g in client.guilds:
        if not os.path.exists('data/servers/{}'.format(str(g.id))):
            os.mkdir('data/servers/{}'.format(str(g.id)))
        p = 'data/servers/{}/settings.json'.format(str(g.id))
        Path(p).touch(exist_ok=True) # If there is no file, make it so.
        if os.path.getsize(p) < 1: # If the file has no data...
            # Make some new data.
            new_data = {
                "name" : g.name
            }
            # Dump it into the file.
            with open(p, 'w') as f:
                dump(new_data, f)

        # User settings.
        # Keep in mind that the generic data must be generic because not all server's users have the same data.
        for u in g.members:
            if not os.path.exists('data/servers/{}/users'.format(str(g.id))):
                os.mkdir('data/servers/{}/users'.format(str(g.id), str(u.id)))
            p = 'data/servers/{}/users/{}.json'.format(str(g.id), str(u.id))
            Path(p).touch(exist_ok=True) # If there is no file, make it so.
            if os.path.getsize(p) < 1: # If the file has no data...
                # Make some new data.
                new_data = {
                    "name" : u.name,
                    "nick" : u.nick
                }
                # Dump it into the file.
                with open(p, 'w') as f:
                    dump(new_data, f)

    log.info("storage.py ready.")

def load_bot_setting(set):
    setting = str(set)
    Path('data/settings.json').touch(exist_ok=True)
    with open('data/settings.json') as file:
        data = json.load(file)
        if setting in data:
            return data[setting]
        else:
            raise NoSuchSettingException


def save_bot_setting(set, val):
    setting = str(set)
    with open('data/settings.json', 'w') as file:
        data = json.load(file)
    with open('data/settings.json', 'w') as file:
        if isinstance(val, datetime.datetime):
            data[setting] = val.isoformat()
        else:
            data[setting] = val
        dump(data, file)


def load_server_setting(id, set):
    setting = str(set)
#    with shelve.open('data/settings') as s:
#        setting = s[str(setting)]
#    return setting
    Path('data/servers/' + str(id) + '/settings.json').touch(exist_ok=True)
    with open('data/servers/' + str(id) + '/settings.json') as file:
        data = json.load(file)
        if setting in data:
            return data[setting]
        else:
            raise NoSuchSettingException


#TODO: Refactor all references to this or set_server_attribute()???
def save_server_setting(id, set, val):
    filestring = 'data/servers/' + str(id) + '/settings.json'
    setting = str(set)
#    with shelve.open('data/settings', writeback=True) as s:
#        if not str(setting) in s:
#            s[str(setting)] = {}
#        s[str(setting)] = str(val)
    with open(filestring, 'r') as file:
        data = json.load(file)
    with open(filestring, 'w') as file:
        if isinstance(val, datetime.datetime):
            log.info('Val was of type datetime.datetime.')
            data[setting] = val.isoformat()
        else:
            data[setting] = val
        dump(data, file)


def get_user_info(sid, uid):
#    with shelve.open('data/user') as s:
#        existing = s[str(id)]
#    return existing
    Path('data/servers/' + str(sid) + '/users/' + str(uid) + '.json').touch(exist_ok=True)
    with open('data/servers/' + str(sid) + '/users/' + str(uid) + '.json') as file:
        data = json.load(file)
        return data


def get_user_attribute(sid, uid, key):
    existing = get_user_info(str(sid), str(uid))
    return existing[key]


def set_user_attribute(sid, uid, key, value):
    #    with shelve.open('data/user', writeback = True) as s:
    #        if not str(id) in s:
    #            s[str(id)] = {}
    #        s[str(id)][key] = value
    with open('data/servers/' + str(sid) + '/users/' + str(uid) + '.json', 'r') as file:
        data = json.load(file)
    with open('data/servers/' + str(sid) + '/users/' + str(uid) + '.json', 'w') as file:
        data[key] = value
        json.dump(data, file)


# What is this for? Do I need it? Can I make it work with JSON instead of shelve?
# Something stupid that I never use. No. Yes, and I did.
def remove_user_attribute(sid: int, uid: int, key: str) -> None:
    #    with shelve.open('data/user', writeback = True) as s:
    #        del s[str(id)][key]
    with open('data/servers/' + str(sid) + '/users/' + str(uid) + '.json', 'r') as file:
        data = json.load(file)
    with open('data/servers/' + str(sid) + '/users/' + str(uid) + '.json', 'w') as file:
        del data[key]
        dump(data, file)


# What?
def get_attribute_for_users(sid: int, key: str) -> list:
    user_list = []
#    with shelve.open('data/user') as s:
#        for id in s:
#            try:
#                user_list.append({"id": id, key: s[id][key]})
#            except KeyError as e:
#                pass
    rec_dir = 'data/servers/' + str(sid) + '/users/'
    for fname in os.listdir(rec_dir):
        with open(rec_dir + fname) as file:
            data = json.load(file)
            try:
                user_list.append({"id": fname[:-5], key: data[key]})
            except KeyError as e:
                # log.error(e.message)
                # what is in this e?
                pass
    return user_list


def get_server_info(id):
#    with shelve.open('data/server') as s:
#        existing = s[str(id)]
#    return existing
    Path('data/servers/' + str(id) + '/settings.json').touch(exist_ok=True)
    with open('data/servers/' + str(id) + '/settings.json') as file:
        data = json.load(file)
        return data


def get_server_attribute(id: int, key: str) -> str:
    existing = get_server_info(str(id))
    return existing[key]


# Attr and Set serve the same purpose in this context... Is this unnecessarily redundant?
def set_server_attribute(id, key, value):
#    with shelve.open('data/server', writeback=True) as s:
#        if not str(id) in s:
#            s[str(id)] = {}
#        s[str(id)][key] = value
    save_server_setting(id, key, value)


# AAAAAH?
# def remove_server_attribute(id, key):
#    with shelve.open('data/server', writeback=True) as s:
#        del s[str(id)][key]


# I'm not sure that I need this.
#def get_attribute_for_servers(key):
#    server_list = []
#    with shelve.open('data/server') as s:
#        for id in s:
#            try:
#                server_list.append({"id" : id, key : s[id][key]})
#            except KeyError as e:
#                pass
#    return server_list
