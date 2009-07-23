import re
from django.utils import simplejson
import urllib, urllib2
from urllib2 import URLError

class EntryParser(object):
    def __init__(self):
        self.model = None
    def parse(self, lines):
        entry = {'notes':""}
        for line in lines:
            matched = False
            for regex, prop in self.regexs:
                match = regex.search(line)
                if match:
                    matched = True
                    entry[prop] = match.group(1).strip()
            if not matched:
                entry['notes'] += line.strip()
        if not entry.has_key('name'): print entry
        return entry

    def submit(self):
        obj = [{"pk":0,
                "model": self.model,
                "fields": {
                    "name": self.name,
                    "creators": creators,
                    "realms": realms,
                    "defunct": self.is_defunct,
                    "closed": self.is_closed,
                    }}]
        json = simplejson.dumps(obj)
        response = self.sendRequest(
            json,
            "http://ckhrysze.net/bards/recall/entry/create/")
        if response: response.close()


class ArmourEntryParser(EntryParser):
    def __init__(self):
        self.model = "bards.armourentry"
        self.regexs = [
            (re.compile("Name:\s+(\S+.*)"), "name"),
            (re.compile("Armour Type:\s*(\w+)"), "type"),
            (re.compile("Overall AC:\s*(\w+.*)"), "ac"),
            (re.compile("Located in:\s*(\w+.*)"), "area"),
            (re.compile("Found on:\s*(\w+.*)"), "mob"),
            (re.compile("Unique:\s*(\w+.*)"), "unique"),
            (re.compile("Special:\S*(\w+.*)"), "special"),
            (re.compile("See Also:\s*(\w+.*)"), "links"),
            ]

class ItemEntryParser(EntryParser):
    def __init__(self):
        self.model = "bards.itementry"
        self.regexs = [
            (re.compile("Name:\s+(\S+.*)"), "name"),
            (re.compile("Item Type:\s*(\w+)"), "type"),
            (re.compile("Located in:\s*(\w+.*)"), "area"),
            (re.compile("Found on:\s*(\w+.*)"), "mob"),
            (re.compile("Unique:\s*(\w+.*)"), "unique"),
            (re.compile("Special:\s*(\S+.*)"), "special"),
            (re.compile("See Also:\s*(\w+.*)"), "links"),
            ]

class WeaponEntryParser(EntryParser):
    def __init__(self):
        self.model = "bards.itementry"
        self.regexs = [
            (re.compile("Name:\s+(\w+.*)"), "name"),
            (re.compile("Damage Type:\s*(\w+)"), "type"),
            (re.compile("Overall WC:\s*(\w+.*)"), "wc"),
            (re.compile("Located in:\s*(\w+.*)"), "area"),
            (re.compile("Found on:\s*(\w+.*)"), "mob"),
            (re.compile("Unique:\s*(\w+.*)"), "unique"),
            (re.compile("Special:\s*(\S+.*)"), "special"),
            (re.compile("See Also:\s*(\w+.*)"), "links"),
            ]

class MonsterEntryParser(EntryParser):
    def __init__(self):
        self.model = "bards.weaponentry"
        self.regexs = [
            (re.compile("Name:\s+(\S+.*)"), "name"),
            (re.compile("Located in:\s*(\w+.*)"), "area"),
            (re.compile("Class:\s*(\w+.*)"), "class"),
            (re.compile("Special:\s*(\S+.*)"), "special"),
            (re.compile("See Also:\s*(\w+.*)"), "links"),
            ]

class AreaEntryParser(EntryParser):
    def __init__(self):
        self.model = "bards.areaentry"
        self.regexs = [
            (re.compile("Name:\s+(\S+.*)"), "name"),
            (re.compile("Coder:\s*(\w+.*)"), 'coder'),
            (re.compile("Realm:\s*(\w+.*)"), 'realm'),
            (re.compile("Level:\s*(\w+.*)"), 'level'),
            ]

class MiscEntryParser(EntryParser):
    def __init__(self):
        self.model = "bards.miscentry"
        self.regexs = [
            (re.compile("Topic:\s+(\S+.*)"), "name"),
            ]
                    

class FileParser(object):
    def __init__(self):
        self.header = re.compile("-+=+\s+(\w+)\s+=+-+")
        self.footer = re.compile("-+=+\s*(?:Last |)[Uu]pdated?:?\s*(.+)\s*=+-+")
        self.func = self.findHeader
        self.entries = []

    def parse(self, file):
        for line in file.readlines():
            self.func(line)
        return self.entries

    def findHeader(self, line):
        match = self.header.search(line)
        if match:
            self.category = match.group(1).lower()
            self.func = self.collectUntilFooter
            self.entry_lines = []

    def collectUntilFooter(self, line):
        match = self.footer.search(line)
        if match:
            self.parseEntry()
            self.func = self.findHeader
        else:
            self.entry_lines.append(line)

    def parseEntry(self):
        entry = parser = None
        if self.category == 'armours':
            parser = ArmourEntryParser()
        elif self.category == 'items':
            parser = ItemEntryParser()
        elif self.category == 'misc':
            parser = MiscEntryParser()
        elif self.category == 'weapons':
            parser = WeaponEntryParser()
        elif self.category == 'monsters':
            parser = MonsterEntryParser()
        elif self.category == 'areas':
            parser = AreaEntryParser()
        if parser: entry = parser.parse(self.entry_lines)
        self.entries.append(entry)


