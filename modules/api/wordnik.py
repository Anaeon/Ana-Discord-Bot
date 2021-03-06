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
    # Get the word.
    req = requests.get('https://api.wordnik.com/v4/words.json/wordOfTheDay?api_key={}'.format(private.wordnik_api_key))
    data = json.loads(req.content)
    f_string = 'Today\'s word: {}'.format(data['word'])
    print(data)
    # Make a pronunciation key.
    hyph_data = get_hyphenation(data['word'])
    print(hyph_data)

    hyph = ''
    if 'error' in hyph_data:
        if hyph_data['statusCode'] == 404:
            hyph = 'Hyphenation data not found (Error 404).)'
        else:
            hyph = 'Unknown. (Error {}))'.format(hyph_data['statusCode'])
    else:
        for i, d in enumerate(hyph_data):
            seg = d['text']
            if 'type' in d:
                if d['type'] == 'stress':
                    seg = seg.upper()
                elif d['type'] == 'secondary stress':
                    seg = '*' + seg + '*'

            hyph = hyph + seg + '-'

    f_string = f_string + '||Pronunciation: (' + hyph[:-1] + ')'

    # Add definitions.
    for i, d in enumerate(data['definitions']):
        f_string = f_string + '||{}: ({}) {}'.format(i + 1, d['partOfSpeech'], d['text'])
    example = get_top_example(data['word'])

    # Add example.
    f_string = f_string + '||Example: "' + example['text'] + '" (Source: ' + example['title'] + ')'
    # f_string = f_string + '||Etymology:{}'.format(get_etymology(data['word']))
    return f_string


def get_top_example(word):
    req = requests.get('https://api.wordnik.com/v4/word.json/{}/topExample?api_key={}'.format(
        word,
        private.wordnik_api_key
    ))
    data = json.loads(req.content)
    return data


def get_hyphenation(word):
    req = requests.get('https://api.wordnik.com/v4/word.json/{}/hyphenation?api_key={}'.format(
        word,
        private.wordnik_api_key
    ))
    data = json.loads(req.content)
    return data
