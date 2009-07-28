import unittest
from mock import Mock
import __builtin__
__builtin__.world = Mock()

import plugin_generator


class PluginGeneratorTest(unittest.TestCase):
    def testDefaultMode(self):
        self.assertTrue(plugin_generator.OnPluginSend("north"))
        self.assertTrue(plugin_generator.OnPluginSend("south"))
        self.assertTrue(plugin_generator.OnPluginSend("east"))
        self.assertTrue(plugin_generator.OnPluginSend("west"))

    def testShipMode(self):
        plugin_generator.setShipMode()
        plugin_generator.OnPluginSend("north")
        world.send.assert_called_with("fore")
        plugin_generator.OnPluginSend("south")
        world.send.assert_called_with("aft")
        plugin_generator.OnPluginSend("east")
        world.send.assert_called_with("starboard")
        plugin_generator.OnPluginSend("west")
        world.send.assert_called_with("port")
        plugin_generator.OnPluginSend("up")
        world.send.assert_called_with("above")
        plugin_generator.OnPluginSend("down")
        world.send.assert_called_with("below")

    def passHolder():
        world.note.assert_called_with("Found room North of Center")
        world.WindowText.assert_called()

def writePlugin(name):
    from jinja2 import FileSystemLoader, Template, Environment

    plugin_dir = "C:/Program Files (x86)/MUSHclient/worlds/plugins/"

    loader = FileSystemLoader("templates")
    env = Environment(loader=loader)
    template = env.get_template("%s.xml" % (name))

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
        writePlugin("KeyPadModes")
