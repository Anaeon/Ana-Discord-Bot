from modules.data import private
from modules.data import misc

import logging
import json
import requests
import xml.etree.ElementTree as ET

frmt = logging.Formatter(misc.LOGGER_FORMATTING)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

c_out = logging.StreamHandler()
c_out.setFormatter(frmt)
log.addHandler(c_out)

def get_etymology(word, useCanonical=False):
    if word is not None:
        req = requests.get('https://api.wordnik.com/v4/word.json/{}/etymologies?api_key={}'.format(
            word,
            private.wordnik_api_key
        ))
        data = json.loads(req.content)
        xml_root = ET.fromstring(str(data[0]))
        f_string = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaa'
        for child in xml_root:
            log.info(child)
            log.info(child.tag)
            log.info(child.attrib)
            for i, a in enumerate(child.attrib):
                log.info(a)
            for atr in child:
                log.info(atr)
                log.info(atr.attrib)
                f_string = f_string + '||{} - {}'.format(child.tag, atr.atrib)
        return f_string
    else:
        return 'Nothing here...'

def get_wotd():
    req = requests.get('https://api.wordnik.com/v4/words.json/wordOfTheDay?api_key={}'.format(private.wordnik_api_key))
    data = json.loads(req.content)
    f_string = 'Today\'s word: {}'.format(data['word'])
    for i, d in enumerate(data['definitions']):
        f_string = f_string + '||{}: ({}) {}'.format(i + 1, d['partOfSpeech'], d['text'])
    # f_string = f_string + '||Etymology:{}'.format(get_etymology(data['word']))
    return f_string
