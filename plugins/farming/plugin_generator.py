import re

# Dark    Flecks  Glisten         Water           Bugs            Weeds/Shrooms
#------------------------------------------------------------------------------
# pale    few     yellow          bone dry        no              very few
# light   some    yellow-green    somewhat damp   some            few
# dark    many    green-yellow    damp            many            bunch
# black   swath   green           soaked          innumerable     a lot

# Air - 'aerate <little|some|lots> <name> air'
# Fertilizer - 'fertilize <little|some|lots> <name> fertilizer'
# Neutralizer - 'spread <little|some|lots> <name> neutralizer'
# Pesticide - 'spray <little|some|lots> <name> pesticide'
# Water - 'water <little|some|lots> <name> water'

class CommandHelper(object):
    def __init__(self):
        self.re_harvest = re.compile("(.*)plant(.*)harvest(.*)", re.DOTALL)
        self.prep_res = [
            (re.compile("(\w)a (\d+)"), 'aerate', 'air',),
            (re.compile("(\w)f (\d+)"), 'fertilize', 'fertilizer',),
            (re.compile("(\w)n (\d+)"), 'spread', 'neutralizer',),
            (re.compile("(\w)p (\d+)"), 'spray', 'pesticide',),
            (re.compile("(\w)w (\d+)"), 'water', 'water',),
            ]

        self.active = True #False

    def packetParse(self, text):
        if self.re_harvest.search(text):
            world.send("harvest")
            self.active = True #False

    def cmdParse(self, cmd):
        global vmetrics
        if cmd == "ftest":
            vmetrics = VisibleMetrics()
            vmetrics.start()
            world.PushCommand
            return "\t"
        else: vmetrics = None

        if cmd[0:5] == "fprep":
            self.prepParse(cmd)
            world.PushCommand
            return "\t"

        return cmd

    def prepParse(self, cmd):
        steps = cmd[6:].split(';')
        for step in steps:
            for prep_re, action, thing in self.prep_res:
                match = prep_re.match(step)
                if match:
                    type = self.parseType(thing, match.group(1))
                    amounts = self.parseAmounts(int(match.group(2)))
                    for amount in amounts:
                        world.send("%s %s %s %s" % (action, amount, type, thing))

    def parseType(self, thing, text):
        if thing == "air":
            if text == "d": return "Detroit"
            if text == "g": return "Genlab"
            if text == "r": return "Ryogi-Pei"
            if text == "s": return "Serinth"
        if thing == "fertilizer":
            if text == "a": return "Alphabet"
            if text == "e": return "Happy Ed's"
            if text == "h": return "Hippie"
            if text == "s": return "Smurfy"
        if thing == "neutralizer":
            if text == "b": return "Burns brand"
            if text == "c": return "Cowville"
            if text == "d": return "Der'thalas"
            if text == "g": return "Garou"
        if thing == "pesticide":
            if text == "a": return "Ant Cave"
            if text == "h": return "Hunch"
            if text == "m": return "Mount"
            if text == "u": return "Murus"
        if thing == "water":
            if text == "a": return "Atlantis"
            if text == "m": return "Gulf of Mexico"
            if text == "r": return "R'lyeh"
            if text == "w": return "Wayhaven"
        return ""
                
    def parseAmounts(self, total):
        amounts = []
        for x in xrange(total/4): amounts.append("lots")
        for x in xrange( (total%4)/2 ): amounts.append("some")
        for x in xrange( (total%2) ): amounts.append("little")
        return amounts

    def sentParse(self, cmd):
        if cmd == "stake claim":
            self.active = True

class Matcher:
    def __init__(self):
        self.matched = False
        self.args = ()
    def __call__(self, *args):
        if args: self.args=args
        if len(self.args)==1:
            if self.args[0]:
                self.matched = True
                return self.translate(self.args[0].group(1).strip())
        return None
    def translate(self, metric):
        if metric == "pale brown": return "pale"
        if metric == "light brown": return "light"
        if metric == "dark brown": return "light"

        elif metric == "very few": return "two"
        elif metric == "a few": return "few"
        elif metric == "a bunch of": return "bunch"
        elif metric == "a swath of": return "swath"
        elif metric == "a lot of": return "lot"

        elif metric == "yellow": return "y"
        elif metric == "yellow-green": return "yg"
        elif metric == "green-yellow": return "gy"
        elif metric == "green": return "g"

        elif metric == "bone dry": return "dry"
        elif metric == "somewhat damp": return "damp"
        elif metric == "damp": return "wet"

        elif metric == "innumerable": return "tons"

        elif metric == "": return ""
        return metric

class VisibleMetrics(object):
    def __init__(self):
        self.re_color = re.compile("The(.+)soil is tinged")
        self.re_gold = re.compile("tinged with(.+)flecks of gold")
        self.re_white = re.compile("gold,(.+) flecks\s+of\s+white")
        self.re_glisten = re.compile("glistens a sickly (.*) colour")
        self.re_water = re.compile("The soil is (.+)\.")
        self.re_bugs = re.compile("This plot of farm has (\w+) bugs.")
        self.re_shrooms = re.compile("This plot of farm has (.*) wild mushrooms.")
        self.re_weeds = re.compile("This plot of farm has (.*) weeds.")

        self.color = None
        self.gold = None
        self.white = None
        self.glisten = None
        self.water = None
        self.bugs = None
        self.shrooms = None
        self.weeds = None

        self.shown = False
        self.parse = self.parseGround

    def start(self):
        self.echo_flag = world.echoinput
        world.echoinput = False
        world.send("look at ground")

    def parseGround(self, text):
        m = Matcher()
        if m(self.re_color.search(text)): self.color = m()
        if m(self.re_gold.search(text)): self.gold = m()
        if m(self.re_white.search(text)): self.white = m()
        if m(self.re_glisten.search(text)): self.glisten = m()
        if m(self.re_water.search(text)): self.water = m()

        self.parse = self.parseBugs
        world.send("look at insects")

        return (self.color and self.gold and self.white and self.glisten and self.water)

    def parseBugs(self, text):
        m = Matcher()
        if m(self.re_bugs.search(text)): self.bugs = m()
        self.parse = self.parseShrooms
        world.send("look at mushrooms")
        return (True and self.bugs)

    def parseShrooms(self, text):
        m = Matcher()
        if m(self.re_shrooms.search(text)): self.shrooms = m()
        self.parse = self.parseWeeds
        world.send("look at weeds")
        return (True and self.shrooms)

    def parseWeeds(self, text):
        m = Matcher()
        if m(self.re_weeds.search(text)): self.weeds = m()
        self.show()
        return (True and self.weeds)

    def cleanup(self):
        world.echoinput = self.echo_flag

    def show(self):
        world.ColourNote("#FFFFFF", "", "Colour\tGold\tWhite\tGlisten\tWater\tBugs\tWeeds\tShrooms")
        world.ColourTell("#FFFFFF", "", "%s\t" % (self.color))
        world.ColourTell("#FFFFFF", "", "%s\t" % (self.gold))
        world.ColourTell("#FFFFFF", "", "%s\t" % (self.white))
        world.ColourTell("#FFFFFF", "", "%s\t" % (self.glisten))
        world.ColourTell("#FFFFFF", "", "%s\t" % (self.water))
        world.ColourTell("#FFFFFF", "", "%s\t" % (self.bugs))
        world.ColourTell("#FFFFFF", "", "%s\t" % (self.shrooms))
        world.ColourTell("#FFFFFF", "", "%s\t" % (self.weeds))
        world.Note("")
        world.Note("")
        self.shown = True

vmetrics = None
cmdhelper = CommandHelper()

def OnPluginPacketReceived(sText):
    global vmetrics
    global cmdhelper
    if cmdhelper:
        cmdhelper.packetParse(sText)
    if vmetrics:
        matched = vmetrics.parse(sText)
        if vmetrics.shown:
            vmetrics.cleanup()
            vmetrics = None
        if matched: return ""
    return sText


def OnPluginCommandEntered(cmd):
    return cmdhelper.cmdParse(cmd)

def OnPluginSent(sText):
    cmdhelper.sentParse(sText)
    return True

