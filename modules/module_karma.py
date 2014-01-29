# -*- encoding: utf8 -*-
#
# TODO:
# - Throttling
# - unfucking the karma message parser (_parse_karma, do_karma)
# - disallowing users to affect their own karma

import re
import sqlite3
import md5 # used for check_delay
import time # used for check_delay
import random # used to choose random item from 'stops'

dudes = [
    "man",
    "dude",
    "buddy",
    "pal",
    "muchacho",
    "caballero",
    "cowboy",
    "sonny",
    "cabron"
]

stops = [
    "Ow",
    "Quit it",
    "Stahp",
    "Stop it",
    "Go away",
    "Beat it",
    "That's enough, now",
    "Nope",
    "That's not going to happen",
    "One more time and I'm out of here",
    "Final warning, no way",
]
karma_delay = 600

# karma_actions is used to check delays for now.
# it's a dictionary of hashes mapped to time.time() values
karma_actions = {}


def check_delay(bot, user, channel, karma_hash):
    """
    checks that <user> hasn't tried to change the karma for <item> in at least <delay>.
    Uses an in-memory hash to check the date
    """
    print "check_delay", karma_hash
    # karma_hash = md5.new(user + item).hexdigest()
    timestamp = time.time()
    # check the time of the previous karma adjustment, if any
    previous_action = karma_actions.get(karma_hash,0)
    
    if timestamp - previous_action > karma_delay:
        karma_actions[karma_hash] = timestamp
        print karma_actions
        return True
    else:
        return False

def do_karma(bot, user, channel, karma):
    """
    perform karma adjustment
    """
    print "::do_karma " + 20 * "-" + "|".join(karma)
    if "++" in karma[0] or "--" in karma[0]:
        # this is the actual karma command. Hack?
        return
    if karma[1] == '++':
        k = 1
    else:
        k = -1

    conn = sqlite3.connect('karma.db')
    c = conn.cursor()
    t = (karma[0].lower(),)
    
    # check the delay
    print "::t=", t[0]
    karma_hash = md5.new(user + t[0]).hexdigest()
    timestamp = time.time()

    if not check_delay(bot, user, channel, karma_hash):
        return bot.say(channel, "%s, %s" % (random.choice(stops), random.choice(dudes)))
        
    c.execute('select * from karma where word=?', t)
    res = c.fetchone()

    if res != None:
        u = k + res[2]
        if u == 0:
            c.execute('delete from karma where word=?', t)
            conn.commit()
            return bot.say(channel, "%s no longer has karma and is garbage collected"  % (karma[0].encode('utf-8', 'replace')))
        else:
            q = (u,karma[0].lower(),)
            c.execute('update karma set karma = ? where word=?', q)
    else:
        u = k
        q = (karma[0].lower(),u,)
        
        c.execute('insert into karma (word, karma) VALUES (?,?)',q)
    
    conn.commit()
        
  
    return bot.say(channel, "%s now has %s karma"  % (karma[0].encode('utf-8', 'replace'), u))


def handle_privmsg(bot, user, reply, msg):
    """Grab karma changes from the messages and handle them"""
    print "::handle_privmsg"
    # m = re.findall('((?u)[\w.`\']+)(\+\+|\-\-)', msg.decode('utf-8'))
    # if len(m) == 0 or len(m) >= 5: return None
    #
    #for k in m:
    #    print "::", k
    #    do_karma(bot, user, reply, k)
    
    """
    This method is used to parse karma from a message.
    It should allow for the following karma syntax:
    thing--
    thing++    
    thing++
    ++thing
    thing1++ thing2++ thing3-- thing4--
    ++thing1 ++thing2 --thing3 --thing4
    thing++ is much better than thing--
    """
    
    # parse the message into tokens
    tokens = msg.split()
    # walk through the tokens

    for token in tokens:
        # is it a ++ or a --?
        if token.find("++")!=-1:
            # there's karma thar
            print "::Adding +1 to %s" % token
            k = token.replace("++","")
            action = "++"
        elif token.find("--")!=-1:
            print "::Subtracting 1 from %s" % token
            k = token.replace("--","")
            action = "--"
        else:
            print "::Ignoring %s" % token
            continue

        do_karma(bot, user, reply, (k, action))
        

def handle_action(bot, user, reply, msg):
    """Grab karma changes from the messages and handle them"""
    print "handle_action"

    m = re.findall('((?u)[\w.`\']+)(\+\+|\-\-)', msg.decode('utf-8'))    
    if len(m) == 0 or len(m) >= 5: return None

    for k in m:
        do_karma(bot, user, reply, k)

    return

def command_karma(bot, user, channel, args):
    """.karma <item>"""
    # return bot.say(channel, "|".join(args))
    print "command_karma: ARGS:", args
    item = args.split()[0]
    if item.find("++")!=-1 or item.find("--")!=-1:
        return
    
    conn = sqlite3.connect('karma.db')
    c = conn.cursor()
    t = (item.lower(),)
    c.execute('select * from karma where word=?', t)
    res = c.fetchone()

    if res != None:
        return bot.say(channel, "%s currently has %s karma" % (item, res[2]))
    else:
        return bot.say(channel, "%s has no karma" % (item))

""" By request of eric, .rank = .karma """
def command_rank(bot, user, channel, args):
    print "command_rank"
    return command_topkarma(bot, user, channel, args)

def command_srank(bot, user, channel, args):
    """ .srank <substring> """
    print "command_srank"
    item = args.split()[0].decode("utf-8")

    conn = sqlite3.connect('karma.db')
    c = conn.cursor()
    t = item.lower()
    c.execute('select word,karma from karma where word like ? order by karma asc', ("%" + item + "%",))
    res = c.fetchall()
    if not len(res):
        return bot.say(channel, unicode("No matches for '*%s*'" % item).encode("utf-8"))
    max_len = 150
    ranks = []

    while len(res):
      new_rank = "%s (%d)" % res.pop()
      if len(", ".join(ranks)) + len(new_rank) < max_len:
        ranks.append(new_rank)
      else:
        break
      
    message = ", ".join(ranks)

    if len(res):
      message = message + " (%d omitted)" % len(res)

    return bot.say(channel, message.encode("utf-8"))



def command_topkarma(bot, user, channel, args):
    """.topkarma"""
    conn = sqlite3.connect('karma.db')
    c = conn.cursor()
    c.execute('select * from karma order by karma desc limit 5')

    for row in c:
        bot.say(channel, "Top 5: %s has %s karma" % (str(row[1]), row[2]))

    return




if __name__ == "__main__":
    messages = """
    thing--
    thing++    
    thing++
    ++thing
    thing1++ thing2++ thing3-- thing4--
    ++thing1 ++thing2 --thing3 --thing4
    thing++ is much better than thing--
    makes Poznan less attractive to me now --that place cost not £, but Pence… and claim European rates.  Can live like a lord out there on Per Diem.  Now it's just a place that is cheap but is a bitch for me to fly to.
    """.split("\n")
    
    for message in messages:
        print message, ":"
        _parse_karma(message)
        