import shelve


class StorageException(Exception):
    """base class for Storage exceptions"""
    pass


class NoSuchAttributeException(StorageException):
    """exception raised when an attribute doesn't exist"""
    pass

class NoSuchSettingException(StorageException):
    """Exception raised when the loaded setting doesn't exist."""
    pass


def load_server_setting(setting):
    with shelve.open('data/settings') as s:
        setting = s[str(setting)]
    return setting


def save_server_setting(setting, val):
    with shelve.open('data/settings', writeback=True) as s:
        if not str(setting) in s:
            s[str(setting)] = {}
        s[str(setting)] = str(val)


def get_user_info(id):
    with shelve.open('data/user') as s:
        existing = s[str(id)]
    return existing


def get_user_attribute(id, key):
    existing = get_user_info(str(id))

    return existing[key]


def set_user_attribute(id, key, value):
    with shelve.open('data/user', writeback = True) as s:
        if not str(id) in s:
            s[str(id)] = {}
        s[str(id)][key] = value


def remove_user_attribute(id, key):
    with shelve.open('data/user', writeback = True) as s:
        del s[str(id)][key]


def get_attribute_for_users(key: object) -> object:
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
        existing = s[str(id)]
    return existing


def get_server_attribute(id, key):
    existing = get_server_info(str(id))

    return existing[key]


def set_server_attribute(id, key, value):
    with shelve.open('data/server', writeback = True) as s:
        if not str(id) in s:
            s[str(id)] = {}
        s[str(id)][key] = value


def remove_server_attribute(id, key):
    with shelve.open('data/server', writeback = True) as s:
        del s[str(id)][key]


def get_attribute_for_servers(key):
    server_list = []
    with shelve.open('data/server') as s:
        for id in s:
            try:
                server_list.append({"id": id, key: s[id][key]})
            except KeyError as e:
                pass
    return server_list
