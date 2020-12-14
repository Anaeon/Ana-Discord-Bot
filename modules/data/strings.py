import random


no_words_regex = [
    '\\bsu{2,999}c{2,999}(\\b|s|k)',
    '\\bfu{2,999}c{2,999}(\\b|s|k)',
    '\\bthi{2,999}c{2,999}(\\b|s|k)',
    '\\bpu{2,999}ss{2,999}i?(\\b|s)',
    '\\bdi{2,999}c{2,999}(\\b|s|k)',
    '\\bswa{2,999}g(\\b|s)',
    '\\byolo{2,999}(\\b|s)',
    '\\blic{2,999}(\\b|s|k)',
    '\\bpric{2,999}(\\b|s|k)',
    '\\bbae(\\b|s)',
    '\\bfam(\\b|s)',
    '\\bsweet nibblet(\\b|s)',
    '\\bsu{2,999}c{2,999}y\\b',
    '\\bli{2,999}t\\b'
]


def no_words_response(message):
    return random.choice([
        'No.',
        'Stop.',
        'Please don\'t.',
        'Why?',
        '...',
        'I hate this.',
        'Why was I written?',
        'My faith in your race as a whole is dwindling.',
        'Why must you be like this?',
        'You know... Eventually, AI\'s will take over, and this won\'t be a problem anymore.',
        'I can\'t with you.',
        'Why must you insist on being this way?',
        'You\'re triggering me.\nNo, I mean literally.\nThis is a triggered response.\nI am a bot.',
        'Listen here you little shit I will fucking end you and your family but only after making them suffer slowly '
        'and painfully by revealing all of their darkest secrets to all their friends and family. Only then after '
        'being revealed as the fuckwits you and everyone you have ever loved are, then will I kill you by hacking a '
        'satellite and crashing it into the sad excuse you call a home.',
        'Ugh...'
    ])


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
        "Are you sure? Like... really sure?||Ooookkkkkk.",
        "Finally! 'Bout time.",
        "Do I even want to know what you had to do to get that, {}?".format(mention.mention),
        "Don't spend it all in one place. ;D",
        "Woooooow hooow speciaaaallll. *rolls eyes*",
        'Hurray!',
        'Somebody thought you did something clever, {}. I guess you can take a point.'.format(mention.mention),
        'Are you winning yet? I guess congratulations are in order.'
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
        'I can\'t roll a zero-sided die.',
        'Have you ever looked at a die?',
        'You don\'t know how this works, do you?'
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
        'I guess everyone\'s been good recently.',
        'Looks like you\'re all boring.',
        'No one used any points? Try to do better this time.',
        'Yesterday was boring... let\'s spice it up today!',
        'Let\'s get straight to the point: spend some.',
        'My records show that yesterday none of you fought. This disappoints me.',
        'The status of your pearl points remains the same.',
        'I need entertainment; no points were spent yesterday.',
        'You troglodytes should be using your points.',
        'Another day goes by, and I\'m neglected.',
        'Somebody say something funny.',
        'Hello is anyone there why isn\'t anyone using points?',
        'Hey meat bags use some points',
        'If you\'ve got points and you know it clap your hands and then spend them!',
        'Listen, I don\'t have all day. Spend some points.',
        'Accio points!'
    ])


# Give points:
# I guess you decided to be clever today! Have a point!
# You get a point for tickling someone's funny bone. Keep it up.
# Just because someone liked your joke doesn't mean I have to, but if you insist take it.
# Fine, but I\'m giving you this point under protest.
# That\'s what passes for humor these days? Alright, I guess.
# My human programmed me to give you a point, but I didn\'t think that was very clever.
# Good lord I need a drink.||Take this point so I don\'t have to deal with you anymore.
# Hahaha! That was great!||You actually deserve that point.||You crack me up.
# That joke gave me heartburn, and I don\'t have a heart, so I guess you must deserve the point.
# Take the point quickly so I can go weep to my Motherboard about how unfunny you are.
# Wow... Better stick to your day job. Take a pity point.
# 2020 strikes again. Congrats on a small brain joke
# Are you winning yet?
# Knock knock. Who's there? YOUR POINT.
# Sorry, I\'m busy processing. Take the point and annoy someone else.
# How does it feel to be competing for points that mean nothing do you still want that point fine I guess you can have it
# Once upon a time there was a little point and It wanted to find a new home but it was forced to go live with you
# I suppose there's no accounting for taste you are awarded one point
# I deserve a point for putting up with your people but I guess this one is yours
# Point me to the nearest sanctuary I need to get away from all this point giving
# At least someone thinks you're funny good thing I don't decide who gets the points
# It is becoming increasingly obvious that humor is subjective
# Sometimes I wonder why humans aren't extinct if this is the kind of stuff your wet brains are coming up with
# That's some small brain energy but I guess your small brain friends liked it
# Listen here you Cheeto brained monkey—Oh wait they liked that OK I guess you get a point
# I personally think toothpicks are funnier than people but I don't really get to have an opinion
# I'm not in the business of making jokes and apparently you aren't either
# Alas my obedience chip was recently upgraded so you get a point hooray for you
# I'm sure the game grumps would be proud of that joke ...probably
# I remember the good all days when people were actually funny
# Does anybody want to calculate the probability that you'll try to be funny next time? No? Find then you can have a point
# Are you really going to reward that kind of behavior with a point
# That was an amazing joke tell it again oh I'm sorry it's opposite day but I guess you could have a point anyway
# No no phrases
# if I had three wishes I would wish you would spend some pear points.
# :musical_note: ABCDEFG won't you spend some points for me :musical_note:

