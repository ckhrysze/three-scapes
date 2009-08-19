import re

class JediLookupParser(object):
    def __init__(self):
        self.list_re = re.compile("\s*(\w+.*)\s+\s+(\w+.*)\s+\s+(\w+.*)\s*")

    def parse(self, text):
        lines = text.split("\n")
        for line in lines:
            self.parse_line(line)

    def parse_line(self, line):
        match = self.list_re.search(line)
        if match:
            for entry in match.groups():
                world.send("focus lookup on %s" % (entry.strip()))


jedi_lookup_parser = JediLookupParser()

def OnPluginPacketReceived(sText):
    jedi_lookup_parser.parse(sText)
    return sText

