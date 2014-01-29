import random

pillow_talks = [
    "You know you love it, %(target)s",
    "So, %(target)s, was it good for you, too?",
    "%(target)s, you were asking for it",
    "%(target)s, stop crying, it's turning me off",
    "%(target)s, blame %(sender)s, he made me do it",
    "%(target)s, now you do me...",
    "ewww, %(target)s, have a mint"
    
]

hugs = [
    "squeezes",
    "wraps his arms around",
    "gives a big, juicy man-hug to",
    "hugs",
    "HUUUUUUUUUUUGS"
]

def command_hug(bot, user, channel, args):
    """
    gives a little hug to who-/whatever
    """
    pillow_talk = random.choice(pillow_talks) 
    sender = user.split("!")[0]
    if len(args)==0 or args=="me":
        target = sender
    else:
        target = args
    hug = "%s %s" % (random.choice(hugs), target)

    print "::command_hug", args
    print "::", len(args)
    print "::", 
    # bot.action(bot.lnick, channel, "Hugs!") # (self, user, channel, data): (source)
    print locals()
    bot.describe(channel, hug )
    print pillow_talk
    # print bot.who(user, channel, [()])
    # bot.names()
    bot.say(channel, pillow_talk % locals())
    
    