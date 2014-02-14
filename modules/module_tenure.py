import urllib2
import csv
import time

TENURE_URL = "https://github.rackspace.com/brint-ohearn/senior-racker/blob/2eeb147e8a2ef29443a4c9951b41f2ed83863be1/tenure.csv"

def get_tenure(victim):
    """
    finds and returns the tenure index for victim
    """
    
    res = csv.reader(urllib2.urlopen("https://github.rackspace.com/brint-ohearn/senior-racker/raw/master/tenure.csv"))
    # victim = " ".join(args)
    print "ffffs", victim
    for row in res:
        if row[1].lower() == victim.lower():
            # we've found our victim
            tenure_idx = int(row[0])
            victim = row[1]
            start_date = time.strptime(row[2], "%Y/%m/%d")
            return "Racker #%d (%s): %s" % (tenure_idx, time.strftime("%d %b %Y", start_date), victim)

    return "'%s' not found" % victim

def command_tenure(bot, user, channel, args):
    """ .tenure Joe Bloggs """
    victim = args
    if victim:
        # res = csv.reader(urllib2.urlopen("http://download.finance.yahoo.com/d/quotes.csv?s=%s&f=sl1d1t1c1p2&e=.csv" % (ticker)).readlines()).next()
        res = get_tenure(victim)
        print res
        return bot.say(channel, res)


if __name__=="__main__":
    import sys
    victim = sys.argv[1:]
    print get_tenure(victim)
    