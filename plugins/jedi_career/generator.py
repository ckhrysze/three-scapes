import re

def parseListing(sText):
    for line in sText.split("\n"):
        match3 = threeCol.search(line)
        match2 = twoCol.search(line)
        if match3:
            world.send("recall %s" % (match3.group(1)))
            world.send("recall %s" % (match3.group(2)))
            world.send("recall %s" % (match3.group(3)))
        elif match2:
            world.send("recall %s" % (match2.group(1)))
            world.send("recall %s" % (match2.group(2)))

def OnPluginPacketReceived(sText):
    if listing.search(sText):
        world.note("Found a listing")
        parseListing(sText)
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
    def send(self, text):
        print "Sent: %s" % (text)
    def note(self, text):
        print text
world = World()

packet1 = """
"""

OnPluginPacketReceived(packet1)


valid_lines = ""
this = open("generator.py", "r")
stopCopy = re.compile("# \*+ NO COPY \*+")
for line in this:
    if stopCopy.match(line) : break
    valid_lines += line


from jinja2 import FileSystemLoader, Template, Environment

loader = FileSystemLoader("templates")
env = Environment(loader=loader)

template = env.get_template("JediCarrer.xml")
f = open("C:/Program Files (x86)/MUSHclient/worlds/plugins/JediCareer.xml", "w")
f.write(template.render(py_script=valid_lines))

