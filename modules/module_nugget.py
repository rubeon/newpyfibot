# -*- coding: utf-8 -*-

from urllib import FancyURLopener
from util.BeautifulSoup import BeautifulSoup
import re
import random

class MyOpener(FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'

class Nuggets():
    def __init__(self):
        self.nugget_list = []
        self.getNuggets()
        self.soup = None
        random.seed()

    def makeSoup(self):
        myopener = MyOpener()
        page = myopener.open(self.url).read()
        self.soup = BeautifulSoup(page)

    def getNuggets(self):
        pass

    def cleanNuggets(self, ugly_nugget_list):
        for nugget in ugly_nugget_list:
            temp = re.sub('<.*?>', '', str(nugget))
            if re.search('\.\.\.', temp): self.nugget_list.append(re.sub('\.\.\.', '', temp))

    def getSentence(self):
        return self.question + self.nugget_list[random.randint(0, len(self.nugget_list) - 1)]

class NuggetsEn(Nuggets):
    def __init__(self, archive_num):
        self.question = "Did you know, "
        #archive_max checked 26-09-2010 http://en.wikipedia.org/wiki/Wikipedia:Recent_additions_1
        self.archive_max = 255
        self.archive_num = archive_num
        if self.archive_num > self.archive_max: self.archive_num = random.randint(1, self.archive_max)
        self.url = "http://en.wikipedia.org/wiki/Wikipedia:Recent_additions_" + str(self.archive_num)
        Nuggets.__init__(self)

    def getNuggets(self):
        self.makeSoup()
        ugly_nugget_list= []
        lists =  self.soup.findAll("ul")
        for list in lists[:-7]:
            for nugget in list.findAll("li"):
                ugly_nugget_list.append(nugget)

        self.cleanNuggets(ugly_nugget_list)

class NuggetsFi(Nuggets):
    def __init__(self, archive_num):
        self.question = "Tiesitkö, että "
        #archive_max checked 13-8-2009
        self.archive_max = 6
        self.archive_num = archive_num
        if self.archive_num > self.archive_max: self.archive_num = random.randint(1, self.archive_max)
        self.url = "http://fi.wikipedia.org/wiki/Wikipedia:Tiesitk%C3%B6_ett%C3%A4.../Arkisto" + str(self.archive_num)
        Nuggets.__init__(self)

    def getNuggets(self):
        self.makeSoup()
        ugly_nugget_list= []
        lists =  self.soup.findAll("ul")
        for nugget in lists[0].findAll("li"):
            ugly_nugget_list.append(nugget)

        self.cleanNuggets(ugly_nugget_list)

class NuggetsNl(NuggetsFi):
    def __init__(self, archive_num):
        self.question = "Wist je dat, "
        #archive_max checked 26-09-2010 http://nl.wikipedia.org/wiki/Wikipedia:Wist_je_dat
        self.archive_max = 52
        self.archive_num = archive_num
        if self.archive_num > self.archive_max: self.archive_num = random.randint(1, self.archive_max)
        self.url = "http://nl.wikipedia.org/wiki/Sjabloon:Hoofdpagina_-_wist_je_dat_" + str(self.archive_num)
        Nuggets.__init__(self)

def command_nugget(bot, user, channel, args):
    """Tells nugget from Wikipedia. Avaible Languages: fi, en, nl Usage: .nugget [lang]"""
    if args:
        if args.lower() == "en":
            nugget = NuggetsEn(10000)
        elif args.lower() == "fi":
            nugget = NuggetsFi(10000)
        elif args.lower() == "nl":
            nugget = NuggetsNl(10000)
        else:
            nugget = None
    else:
        nugget = NuggetsEn(10000)

    if nugget != None:
        msg = nugget.getSentence()
    else:
        msg = "Sorry, I don't speak the language '%s'" % str(args)

    return bot.say(channel, msg)
