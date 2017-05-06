import requests
import json
#  import random
import re


def get_quote():
    # req = requests.get('https://api.whatdoestrumpthink.com/api/v1/quotes/')
    req = requests.get('https://api.whatdoestrumpthink.com/api/v1/quotes/random')
    data = json.loads(req.content)
    msg = data['message']
    msg = re.sub('`', r'\'', msg)
    # return random.choice(data['messages']['non_personalized'])
    return msg


def get_personal_quote(person):
    pass
