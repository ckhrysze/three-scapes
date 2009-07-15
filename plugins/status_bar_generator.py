import re

class BarField(object):
    def __init__(self, title, pattern, color = 0x00FF00, max = 100, current = 0):
        self.title = title
        self.pattern = pattern
        self.color = color
        self.max = 100
        self.current = 0

    def match(self, sText):
        result = self.pattern.search(sText)
        if not result : return False

        self.current = result.group(1)
        self.max = result.group(2)
        return True

    def render(self, window, left, top, right, bottom):
        maxHeight = bottom - top
        scaled = ( float(maxHeight) / float(self.max) ) * float(self.current)
        current = maxHeight - int(scaled)
        world.WindowRectOp(window, 1, left, top, right, bottom, self.color, 0x0000FF)
        world.WindowRectOp(window, 2, left, current, right, bottom, self.color, 0x0000FF)

class PercentBarField(object):
    def __init__(self, title, pattern, color = 0x00FF00, percent = 100.0):
        self.title = title
        self.pattern = pattern
        self.color = color
        self.percent = percent

    def match(self, sText):
        result = self.pattern.search(sText)
        if not result : return False

        self.percent = float(result.group(1))
        if (result.lastindex > 1):
            self.percent += (float(result.group(2)) / 100.0)
        return True

    def render(self, window, left, top, right, bottom):
        maxHeight = bottom - top
        current = maxHeight - int((float(maxHeight) / float(100)) * float(self.percent))
        world.WindowRectOp(window, 1, left, top, right, bottom, self.color, 0x0000FF)
        world.WindowRectOp(window, 2, left, current, right, bottom, self.color, 0x0000FF)

class TextField(object):
    def __init__(self, title, pattern, titleColor = 0xFFFFFF, color = 0xFFFFFF, text = ""):
        self.title = title
        self.pattern = pattern
        self.titleColor = titleColor
        self.color = color
        self.text = text

# Your great speed allows you to attack again!
# **THWACK** You critically hit A young professor is here, researching sociology!
class MyAttackFields(object):
    """
    You bobble your swing
    Your blow was deflected
    You tickled Professor in the stomach
    You grazed Professor
    You hit Professor
    You hit Professor very hard
    You struck Student a mighty blow
    You smashed Scholar with a bone crushing sound
    You pulverized Scholar with a powerful attack

    """
    def __init__(self, color = 0xFFFFFF):
        self.text = "Hello!"
        self.color = color

        self.combat_rounds = 0
        self.total_rounds = 0
        self.in_combat = False

        self.killing_blow_pattern = re.compile("dealt the killing blow")
        self.gxp_pattern = re.compile("GXP:(\d+)")

        self.gxp = 0.0
        self.avg_gxp_session = 0.0
        self.avg_gxp_rnd = 0.0
        self.gxp_diff = 0.0

    def reset(self):
        self.total_rounds = 0
        self.combat_rounds = 0
        self.avg_gxp_session = 0
        self.avg_gxp_rnd = 0

    def match(self, sText):
        result = self.gxp_pattern.search(sText)
        if not result: return False

        gxp = float(result.group(1))
        if self.gxp == 0: self.gxp = gxp

        self.gxp_diff = self.gxp - gxp
        previous_total = self.avg_gxp * self.rounds
        new_total = previous_total + self.gxp_diff
        self.rounds += 1
        self.avg_gxp = float(new_total) / float(self.rounds)
        self.gxp = gxp
        return True

    def render(self, window, left, abs_top):
        top = abs_top
        world.WindowText(window, "f", "rounds  : %s" % (self.rounds), left, top, 0, 0, self.color, False)
        top += 15
        world.WindowText(window, "f", "rnd gxp : %s" % (self.gxp_diff), left, top, 0, 0, self.color, False)
        top += 15
        world.WindowText(window, "f", "avg gxp : %s" % (self.avg_gxp), left, top, 0, 0, self.color, False)

#HP:254/266 SP:201/218 K:131/131 V:100 S:0;93% [[ HS:2 ]] GXP:4489  T:Dea
class UrlonStats(object):
    def __init__(self):
        self.hp = BarField("HP", re.compile("HP:(\d+)/(\d+)"), color = 0x00FF00)
        self.sp = BarField("SP", re.compile("SP:(\d+)/(\d+)"), color = 0xFF3333)
        self.karma = BarField("K", re.compile("K:(\d+)/(\d+)"), color = 0x99FF66)
        self.voice = BarField("V", re.compile("V:(\d+)/(\d+)"), color = 0xAAFFFF)
        self.combat = MyAttackFields()

    def match(self, sText):
        self.hp.match(sText)
        self.sp.match(sText)
        self.karma.match(sText)
        self.voice.match(sText)
        self.combat.match(sText)

    def reset(self):
        self.combat.reset()

    def render(self, window, width, height):
        self.hp.render(window, 0, 0, 20, height)
        self.sp.render(window, 25, 0, 45, height)
        self.karma.render(window, 50, 0, 70, height)
        self.voice.render(window, 75, 0, 95, height)
        self.combat.render(window, 105, 5)

stats = None

def OnPluginInstall():
    global stats
    stats = UrlonStats()
    win = world.GetPluginID
    height = world.GetInfo(280)
    width = 400
    world.WindowCreate(win, 0, 0, width, height, 6, 0, 0x000000)
    world.WindowFont(win, "f", "Bitstream Vera Sans Mono", 11, True, False, False, False, 1, 0)

def OnPluginClose():
    win = world.GetPluginID
    world.WindowDelete(win)

def OnPluginConnect():
    stats.reset()

def OnPluginPacketReceived(sText):
    win = world.GetPluginID
    height = world.GetInfo(280)
    width = 400
    world.WindowCreate(win, 0, 0, width, height, 6, 0, 0x000000)
    world.WindowShow(win, 1)

    matched = []
    stats.match(sText)
    stats.render(world.GetPluginID, width, height)
    return sText


# **************************** NO COPY ******************************


class World(object):
    def __init__(self):
        self.GetWorldWindowPosition = "0,0,100,100"
    def GetPluginID():
        return "1"
    def WindowDelete(self, id):
        pass
    def WindowCreate(self, win, left, top, right, bottom, mode, position, color):
        pass
    def WindowRectOp(self, win, mode, left, top, right, bottom, color1, color2):
        pass
    def WindowShow(self, win, status):
        pass
    def WindowFont(self, *args):
        pass
    def WindowText(self, *args):
        pass
    def GetInfo(self, code):
        return 300
    def note(self, text):
        print text
world = World()

OnPluginInstall()

packet = """
HP:254/266 SP:201/218 K:131/131 V:100/100 S:0;93% [[ HS:2 ]] GXP:4489  T:Dea
"""
packet2 = """
You pulverized Patron with a powerful attack.
"""
OnPluginPacketReceived(packet)
OnPluginPacketReceived(packet2)

valid_lines = ""
this = open("status_bar_generator.py", "r")
stopCopy = re.compile("# \*+ NO COPY \*+")
for line in this:
    if stopCopy.match(line) : break
    valid_lines += line


from jinja2 import FileSystemLoader, Template, Environment

loader = FileSystemLoader("templates")
env = Environment(loader=loader)
template = env.get_template("StatusBars.xml")

f = open("C:/Program Files (x86)/MUSHclient/worlds/plugins/UrlonStats.xml", "w")
f.write(template.render(py_script=valid_lines))

