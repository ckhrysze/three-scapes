import unittest
from mock import Mock
import __builtin__
__builtin__.world = Mock()

import plugin_generator as pg


class PluginGeneratorTest(unittest.TestCase):
    def testDirections(self):
        pg.OnPluginCommandEntered("_to_road_portal")
        world.EvaluateSpeedwalk.assert_called_with("12n (leave/enter) 8n 4e 6n 9w")

    def testReverseDirectionsWithFrom(self):
        pg.OnPluginCommandEntered("_from_road_portal")
        world.ReverseSpeedwalk.assert_called_with("12n (leave/enter) 8n 4e 6n 9w")

    def testReverseDirectionsWithReverse(self):
        pg.OnPluginCommandEntered("_reverse_road_portal")
        world.ReverseSpeedwalk.assert_called_with("12n (leave/enter) 8n 4e 6n 9w")

    def testShowDirections(self):
        pg.OnPluginCommandEntered("_show_road_portal")
        world.Note.assert_called_with("12n (leave/enter) 8n 4e 6n 9w")

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
        writePlugin("Directions")
