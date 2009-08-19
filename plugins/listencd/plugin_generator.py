import re

class ListenCDMode(object):
    def __init__(self):
        self.active = False
        self.mappings = (
            [re.compile("A small dark cave somewhere in the Scottish highlands"),
             "sing Several Species of Small Furry Animals Gathered Together in a Cave and Grooving with a Pict"],
            [re.compile("A one way street"), "sing superman"],
            [re.compile("A Strange, Strange Shop"), "sing house of fun"],
            [re.compile("A strange place"), "sing always look on the bright side of life"],
            [re.compile("Floating in mid-air"), "sing why does it always rain on me"],
            [re.compile("An endless pink expanse"), "sing blister in the sun"],
            [re.compile("On a shabby street"), "sing in the ghetto"],
            [re.compile("A heart-shaped room"), "sing shape of my heart"],
            [re.compile("In a jungle"), "sing the lion sleeps tonight"],
            [re.compile("In a lab"), "sing monster mash"],
            [re.compile("Argh\!  People everywhere\!"), "sing absolutely everybody"],
            [re.compile("Outside a house"), "sing blue"],
            [re.compile("The Peach State"), "sing the devil went down to georgia"],
            [re.compile("A swamp"), "sing joy to the world"],
            [re.compile("Beneath a summer sky"), "sing 99 red balloons"],
            [re.compile("Floating in a starry sky"), "sing drops of jupiter"],
            [re.compile("Beside a River"), "answer "],
            [re.compile("The golem tells you: Right!  Well done."), "sing the riddle"],
            )
    def activate(self):
        self.active = True
        world.note("Listen CD mode now active")
    def deactivate(self):
        self.active = False
        world.note("Listen CD mode now inactive")
    def parse(self, text):
        for regex, cmd in self.mappings:
            if regex.search(text):
                world.setcommand(cmd)

listencd = ListenCDMode()

def OnPluginPacketReceived(sText):
    if listencd.active: listencd.parse(sText)

def OnPluginSent(sText):
    if re.match("listen cd", sText): listencd.activate()
    if re.match("enter doorway", sText): listencd.deactivate()
    return True
