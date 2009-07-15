import re
from mockworld import World

world = World()

class Area(object):
    def __init__(self, creators, name, realms, closed, defunct):
        self.creators = creators
        self.name = name
        self.realms = realms
        self.is_closed = closed
        self.is_defunct = defunct

    def __str__(self):
        return self.name
    def __repr__(self):
        return self.__str__()

def parse(lines):
    num = creators = name = realms = ""
    closed = defunct = False
    for line in lines:
        num += line[0:8]
        creators += line[8:28] + " "
        name += line[29:64] + " "
        realms += line[65:] + " "

    area_creators = [creator.strip() for creator in re.split("\W+", creators.strip())]
    while 'and' in area_creators: area_creators.remove('and')

    area_realms = [realm.strip() for realm in realms.strip().split()]
    while 'and' in area_realms: area_realms.remove('and')

    if '(CLOSED)' in area_realms:
        area_realms.remove('(CLOSED)')
        closed = True
    if '(DEFUNCT)' in area_realms:
        area_realms.remove('(DEFUNCT)')
        defunct = True

    return Area(area_creators, name.strip(), area_realms, closed, defunct)

def scan(lines):
    entry = re.compile("^\s*\d+\.\s+\w+.*$")
    more = re.compile("^More: \d+-\d+\(\d+\).*$")
    end = re.compile("^>\s+$")

    areas = []
    area_lines = []
    for line in lines:
        if end.match(line) or more.match(line):
            print "matched end or more"
            if len(area_lines) > 0: areas.append(parse(area_lines))
        elif entry.match(line):
            if len(area_lines) > 0: areas.append(parse(area_lines))
            area_lines = [line]
        else:
            if len(area_lines) > 0: area_lines.append(line)
    return areas
