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


def get_wotd(raw=False):
    # Get the word.
    req = requests.get('https://api.wordnik.com/v4/words.json/wordOfTheDay?api_key={}'.format(private.wordnik_api_key))
    data = json.loads(req.content)
    if raw:
        return '```json\n' + str(data) + '\n```'
    f_string = 'Today\'s word: {}'.format(data['word'])
    # Make a pronunciation key.
    print('data ' + str(type(data)))
    hyph_data = get_hyphenation(data['word'])

    hyph = ''
    print('hyph_data' + str(type(hyph_data)))
    if isinstance(hyph_data, dict):
        if hyph_data['statusCode'] != 404:
            for i, d in enumerate(hyph_data):
                print('hyph_data[' + str(i) + ']' + str(type(d)))
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
        partOfSpeech = ''
        if 'partOfSpeech' in d:
            partOfSpeech = d['partOfSpeech']
        else:
            partOfSpeech = '???'

        f_string = f_string + '||{}: ({}) {}'.format(i + 1, partOfSpeech, d['text'])
    example = get_top_example(data['word'])

    # Add example.
    f_string = f_string + '||Example: "' + example['text'] + '" (Source: ' + example['title'] + ')'
    # f_string = f_string + '||Etymology:{}'.format(get_etymology(data['word']))

    if data['note'] is not None:
        f_string = f_string + '||Note: ' + data['note']
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
