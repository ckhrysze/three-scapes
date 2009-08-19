import unittest
from mock import Mock
import __builtin__
__builtin__.world = Mock()

import plugin_generator as pg


def sendGroundPacket():
    pg.OnPluginPacketReceived(
        "The light brown soil is tinged with some flecks of gold, a few " +
        "flecks of white, and glistens a sickly yellow-green colour.  The " +
        "soil is bone dry.")
def sendBugPacket():
    pg.OnPluginPacketReceived(
        "> This plot of farm has many bugs.")
def sendShroomPacket():
    pg.OnPluginPacketReceived(
        "> This plot of farm has a bunch of wild mushrooms.")
def sendWeedPacket():
    pg.OnPluginPacketReceived(
        "> This plot of farm has very few weeds.")
class PluginGeneratorTest(unittest.TestCase):

    def shouldStartsInParseGround(self):
        pg.OnPluginCommandEntered("ftest")
        self.assertEquals(pg.vmetrics.parse, pg.vmetrics.parseGround)

    def shouldParsesGroundMetrics(self):
        pg.OnPluginCommandEntered("ftest")
        sendGroundPacket()
        self.assertEquals("light", pg.vmetrics.color)
        self.assertEquals("some", pg.vmetrics.gold)
        self.assertEquals("few", pg.vmetrics.white)
        self.assertEquals("yg", pg.vmetrics.glisten)
        self.assertEquals("dry", pg.vmetrics.water)
        self.assertEquals(pg.vmetrics.parse, pg.vmetrics.parseBugs)
        world.send.assert_called_with("look at insects")

    def shouldParsesBugMetric(self):
        pg.OnPluginCommandEntered("ftest")
        sendGroundPacket()
        sendBugPacket()
        self.assertEquals("many", pg.vmetrics.bugs)
        self.assertEquals(pg.vmetrics.parse, pg.vmetrics.parseShrooms)
        world.send.assert_called_with("look at mushrooms")

    def shouldParsesShroomMetric(self):
        pg.OnPluginCommandEntered("ftest")
        sendGroundPacket()
        sendBugPacket()
        sendShroomPacket()
        self.assertEquals("bunch", pg.vmetrics.shrooms)
        self.assertEquals(pg.vmetrics.parse, pg.vmetrics.parseWeeds)
        world.send.assert_called_with("look at weeds")

    def shouldParsesWeedsMetric(self):
        pg.OnPluginCommandEntered("ftest")
        sendGroundPacket()
        sendBugPacket()
        sendShroomPacket()
        sendWeedPacket()
        world.ColourNote.assert_called_with("#FFFFFF", "", "Colour\tGold\tWhite\tGlisten\tWater\tBugs\tWeeds\tShrooms")
        world.ColourTell.assert_called()
        self.assertTrue(pg.vmetrics == None)

    def shouldSendHarvest(self):
        pg.OnPluginSent("stake claim")
        pg.OnPluginPacketReceived(
            "The plant shivers, nudges, and moves its leaves into\n" +
            "its final position to be harvested!")
        world.send.assert_called_with("harvest")

    def shouldParseFertilizerCommands(self):
        __builtin__.world = Mock()
        pg.OnPluginSent("stake claim")
        pg.OnPluginCommandEntered("fprep hf 7")
        self.assertEquals(3, world.send.call_count)

    def shouldParseWaterCommands(self):
        __builtin__.world = Mock()
        pg.OnPluginSent("stake claim")
        pg.OnPluginCommandEntered("fprep aw 9")
        self.assertEquals(3, world.send.call_count)

    def shouldParseMultipleCommands(self):
        __builtin__.world = Mock()
        pg.OnPluginSent("stake claim")
        pg.OnPluginCommandEntered("fprep aw 9;hp 12;cn 7;sf 10;da 12")
        self.assertEquals(15, world.send.call_count)

    #def shouldDoNothingWhenInactive(self):
    #    pg.vmetrics = None
    #    pg.OnPluginPacketReceived(
    #        "The plant shivers, nudges, and moves its leaves into" +
    #        "its final position to be harvested!")

        

def writePlugin(name):
    from jinja2 import FileSystemLoader, Template, Environment

    plugin_dir = "C:/Program Files (x86)/MUSHclient/worlds/plugins/"

    loader = FileSystemLoader("templates")
    env = Environment(loader=loader)
    template = env.get_template("plugin.xml")

    plugin_source = open("plugin_generator.py", "r")
    lines = ""
    for line in plugin_source.readlines():
        lines += line
    plugin_output = open("%s/%s.xml" % (plugin_dir, name), "w")
    plugin_output.write(template.render(py_script=lines))

if __name__ == '__main__':
    loader = unittest.TestLoader()
    loader.testMethodPrefix = "should"
    suite = loader.loadTestsFromTestCase(PluginGeneratorTest)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        print "Errors found, plugin not generated"
    else:
        writePlugin("Farming")
