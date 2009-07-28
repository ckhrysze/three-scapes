import re

class AreaMap(object):
    def __init__(self):
        self.top_lines = []
        self.mid_line = "@"
        self.bottom_lines = []

    def draw(self, window, left, midY):
        world.WindowText(window, "f", self.mid_line, left, midY, 0, 0, 0xFFFF00, False)
        

class Room(object):
    def __init__(self):
        self.title = ""
        self.desc = []
        self.areamap = AreaMap()

    def draw(self, window):
        #world.WindowText(window, "f", "r", 0, 0, 0, 0, 0xFFFFFF, False)
        self.areamap.draw(window, 0, 200)

class RoomParser(object):
    def __init__(self):
        self.title_re = re.compile("^(\w+.*)\(.*\)(.*)$")
        self.desc_re = re.compile("^(\[(.)*?m)\w+")
        self.end_re = re.compile("^>\s*$")
        self.exit_res = [
            re.compile("No obvious exits."),
            re.compile("There is one obvious exit"),
            re.compile("There are (\w+) obvious exits"),
            ]
        self.reset()

    def reset(self):
        self.room = Room()
        self.parseNext = self.parseTitle

    def parsePacket(self, packet, callback):
        self.roomCompleteCallback = callback
        lines = packet.split("\n")
        for line in lines:
            self.parseNext(line)

    def parseTitle(self, line):
        match = self.title_re.search(line)
        if match:
            self.room.title = match.group(1).strip()
            world.note("Found room %s" % (self.room.title))
            self.room.areamap.mid_line = match.group(2)
            self.parseNext = self.parsePostTitleHeader
        else:
            self.room.areamap.top_lines.append(line)

    def parsePostTitleHeader(self, line):
        match = self.desc_re.search(line)
        if match:
            self.parseNext = self.parseDesc
            self.parseDesc(line)
        else:
            self.room.areamap.bottom_lines.append(line)

    def parseDesc(self, line):
        for exit_re in self.exit_res:
            match = exit_re.search(line)
            if match:
                self.parseNext = self.parseEnd
                return
        if line.strip():
            self.room.desc.append(line)

    def parseEnd(self, line):
        match = self.end_re.search(line)
        if match:
            self.roomCompleteCallback(self.room)
            self.reset()

roomParser = RoomParser()
def OnPluginInstall():
    win = world.GetPluginID
    world.WindowDelete(world.GetPluginID)
    height = world.GetInfo(280)
    width = 400
    world.WindowCreate(win, 0, 0, width, height, 6, 0, 0x000000)
    world.WindowFont(win, "f", "Bitstream Vera Sans Mono", 11, True, False, False, False, 1, 0)
    world.WindowShow(win, 1)
    AreaMap().draw(win, 10, 200)

def OnPluginClose():
    global roomParser
    roomParser = None
    world.WindowDelete(world.GetPluginID)

def OnPluginConnect():
    pass

def OnPluginEnable():
    global roomParser
    roomParser = RoomParser()

def OnPluginDisable():
    world.WindowDelete(world.GetPluginID)
    global roomParser
    roomParser = None

def OnPluginPacketReceived(sText):
    #roomParser.parsePacket(sText, processRoom)
    return sText

def processRoom(room):
    room.draw(world.GetPluginID)
