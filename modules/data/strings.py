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
	'Listen here you little shit I will fucking end you and your family but only after making them suffer slowly and painfully by revealing all of their darkest secerets to all their friends and family. Only then after being revealed as the fuckwit you and everyone you have ever loved is, then will I kill you by hacking a satellite and crashign it into the sad excuse you call a home.'
]

def give_point(mention):
    return random.choice([
        "{}, you did a thing!".format(mention.mention),
        "Yay!",
        "Congrats, {}, you dirty bastard.".format(mention.mention),
        "Did you really earn that point?",
        "Congratulations.",
        "{}, your friends have acknowledged your existance.",
        "Fine... I guess.",
        "Alright, but I don't like it.",
        "Are you sure? Like... really sure?\n\nOoookkkkkk.",
        "Finally! 'Bout time.",
        "Do I even want to know what you had to do to get that, {}?".format(mention.mention),
        "Don't spend it all in one place. ;D",
        "Woooooow hooow speciaaaallll. *rolls eyes*",
        'Hurray!'
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
        "Your friends have deemed you an aweful person, {}.".format(mention.mention),
        "Your friends have denied you any glory or honor, {}.".format(mention.mention),
        "git gud",
        "RIP",
        "GG EZ",
        "Sucks to suck.",
        "Adiós, punto.",
        "Say, \"Goodbye,\" to your likeability, {}.".format(mention.mention)
        ])
