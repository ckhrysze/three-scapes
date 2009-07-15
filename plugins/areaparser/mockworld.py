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
