import unittest
from mock import Mock
import __builtin__
__builtin__.world = Mock()

import plugin_generator


class PluginGeneratorTest(unittest.TestCase):
    def testActivateOnListenCD(self):
        plugin_generator.OnPluginSent("listen cd")
        world.note.assert_called_with("Listen CD mode now active")

    def testDectivateOnEnterDoorway(self):
        plugin_generator.OnPluginSent("enter doorway")
        world.note.assert_called_with("Listen CD mode now inactive")

    def testPictSong(self):
        plugin_generator.OnPluginSent("listen cd")
        plugin_generator.OnPluginPacketReceived("A small dark cave somewhere in the Scottish highlands")
        world.setcommand.assert_called_with("sing Several Species of Small Furry Animals Gathered Together in a Cave and Grooving with a Pict")

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
    suite = unittest.TestLoader().loadTestsFromTestCase(PluginGeneratorTest)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        print "Errors found, plugin not generated"
    else:
        writePlugin("ListenCD")
