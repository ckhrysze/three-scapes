import re


class Revealer(object):

    def __init__(self):
        self.prepared = False
        self.regexs = (
            (re.compile(".*You finish studying .*\, and.*"), self.success),
            (re.compile(".*You finish studying .*\, but decide.*"), self.skip),
            (re.compile(".*You finish studying .*\, but.*"), self.failure),
            (re.compile("Syntax\: reveal \<item\>\, where \<item\> .*"), self.error),
            )

    def prepare(self, world, items):
        self.prepared = True
        self.current = 0
        self.revealed = []

        self.world = world
        self.items = []
        for item in items:
            if not item in self.items:
                self.items.append(item)
            else:
                i = 1
                while True:
                    i += 1
                    indexed = "%s %s" % (item, i)
                    if not indexed in self.items:
                        self.items.append(indexed)
                        break
                    
    def packetReceived(self, text):
        for line in text.split("\n"):
            for pattern, func in self.regexs:
                if pattern.match(line):
                    func()
                    return

    def start(self):
        world.note("Will attempt to reveal: %s" % self.items)
        self.next()

    def failure(self):
        self.next()

    def skip(self):
        self.current += 1
        self.next()

    def error(self):
        world.note("skipping %s, bad command" % self.items[self.current])
        self.current += 1
        self.next()

    def success(self, name=None):
        self.revealed.append("%s => %s" % (self.items[self.current], name))
        self.current += 1
        self.next()

    def next(self):
        if self.current >= len(self.items):
            self.cleanup()
        else:
            world.note("Next item: %s " % self.items[self.current])
            world.send("reveal %s" % self.items[self.current])

    def cleanup(self):
        self.prepared = False
        world.note("%s" % self.revealed)

        
revealer = Revealer()

def revealAll(name, line, wildcards):
    items = line.split(" ")[1:]
    revealer.prepare(world, items)
    revealer.start()

def toggleRevealer(name, line, wildcards):
    revealer.prepared = not revealer.prepared
    world.note("Revealer is now: %s" % revealer.prepared)

def OnPluginPacketReceived(sText):
    if revealer.prepared:
        revealer.packetReceived(sText)
    return sText

