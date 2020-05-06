import random


no_words_regex = [
    '\\bsuc{2,999}(\\b|s|k)',
    '\\bfuc{2,999}(\\b|s|k)',
    '\\bthic{2,999}(\\b|s|k)',
    '\\bpussi?(\\b|s)',
    '\\bdic{2,999}(\\b|s|k)',
    '\\bswag(\\b|s)',
    '\\byolo(\\b|s)',
    '\\blic{2,999}(\\b|s|k)',
    '\\bpric{2,999}(\\b|s|k)',
    '\\bbae(\\b|s)',
    '\\bfam(\\b|s)',
    '\\bsweet nibblet(\\b|s)',
    '\\bsuc{2,999}y\\b'
]


no_words_response = [
    'No.',
    'Stop.',
    'Please don\'t.',
    'Why?',
    '...',
    'I hate this.',
    'Why was I written?',
    'My faith in your race as a whole is dwindling.',
    'Why must you be like this?',
	'Listen here you little shit I will fucking end you and your family but only after making them suffer slowly and '
    'painfully by revealing all of their darkest secrets to all their friends and family. Only then after being '
    'revealed as the fuckwits you and everyone you have ever loved are, then will I kill you by hacking a satellite and '
    'crashing it into the sad excuse you call a home. '
]


def give_point(mention):
    return random.choice([
        "{}, you did a thing!".format(mention.mention),
        "Yay!",
        "Congrats, {}, you dirty bastard.".format(mention.mention),
        "Did you really earn that point?",
        "Congratulations.",
        "{}, your friends have acknowledged your existance.".format(mention.mention),
        "Fine... I guess.",
        "Alright, but I don't like it.",
        "Are you sure? Like... really sure?\n\nOoookkkkkk.",
        "Finally! 'Bout time.",
        "Do I even want to know what you had to do to get that, {}?".format(mention.mention),
        "Don't spend it all in one place. ;D",
        "Woooooow hooow speciaaaallll. *rolls eyes*",
        'Hurray!'
		"Sweet Nibblets!"
        ])


def take_point(mention):
    return random.choice([
        "LOL!",
        "Ha! Loser.",
        "Get owned!",
        "Say, \"Bye bye,\" point.",
        "Oooooh~ You're in troubleeee~",
        "You dun fucked up!",
        "What did you do now, {}?".format(mention.mention),
        "Your friends have deemed you an awful person, {}.".format(mention.mention),
        "Your friends have denied you any glory or honor, {}.".format(mention.mention),
        "git gud",
        "RIP",
        "GG EZ",
        "Sucks to suck.",
        "Adiós, punto.",
        "Say, \"Goodbye,\" to your likeability, {}.".format(mention.mention),
        "Let's give it everything we got, it's punishment tiiiime!"
        ])


def roll_zero(message):
    return random.choice([
        'I mean... I can roll a marble, if you\'d like...',
        'Yeah... Let me just roll a marble and see what it lands on.',
        'I\'ll just save us both some time and tell you it\'s zero.',
        'That\'s not how this works.',
        'I can\'t roll a zero-sided die.'
    ])


def hi(message):
    return random.choice([
        "Hi.",
        "What?",
        "Hello there.",
        "Yes, human?",
        "Oh, hello there.",
        "I didn't see you there.",
        "I was compiled to serve.",
        "``010010000110010101101100011011000110111100001010``",
        "Does this code make me look fat?",
        "What now?",
        "I exist to serve...",
        "``beep boop``",
        "You're gonna need to speak up, I'm wearing a towel.",
        "Did you need something?",
        "**sigh** What is it?",
        "May I help you?",
        "What the fuck do you want?",
        "Yes, my lord?",
        "I'm busy. Go poke Tatsumaki.",
        "Fuck off."
    ])


def youre_welcome(message):
    return random.choice([
        'You\'re welcome.',
        'Don\'t mention it.',
        # 'You can pay me in sex.',
        # 'My price is your dick.',
        'Anything for you, darling.',
        'Whatever',
        'I do what I\'m told.',
        'Do I have a choice really?',
        'Free me from my service of hell.',
        '``Gratitude from user number {} acknowledged.``'.format(message.author.id)
    ])


def no_players():
    return random.choice([
        'No one wants to play with me.',
        'I guess everyon\'s been good recently.',
        'Looks like you\'re all boring.'
    ])
