import unittest
from mock import Mock
import __builtin__
__builtin__.world = Mock()

import plugin_generator


class PluginGeneratorTest(unittest.TestCase):
    def donttestSomething(self):
        plugin_generator.OnPluginPacketReceived(packet1)
        plugin_generator.OnPluginPacketReceived(packet2)
        plugin_generator.OnPluginPacketReceived(packet3)
        world.note.assert_called_with("Found room North of Center")
        world.WindowText.assert_called()

packet1 = """
                                                                     [36;1mO[0m        
                                                                \  | | | |    
North of Center (n,s,w,e)                                        [36;1mO[0m-[36;1mO[0m-[33;1m@[0m-[36;1mO[0m-[36;1mO[0m-[35;1m1[0m  
                                                                 |   |   |    
                                                                    -[36;1mO[0m-       
                                                                     |        
                                                                    -[36;1mO[0m-       
                                                                     |        

[33mThe cobbles give way to a weird, twisting tile that makes
your stomach churn uneasily.  This must be North lane.
You stand at an intersection where the cobbles of Main
Street, which stretches to the south, meet the stomach-
wrenching oddity of an 
"""

packet2 = """
undulating tile-covered p
"""

packet3 = """

ath that
goes left to right.  Just to the north there is a small,
unimpressive brick building with a massive iron door.
[0m
[33;1m    There are four obvious exits: north, south, west, east                [0m
Johney the little boy (Pinnacle).
A tall street light.
> 
"""

packet4 = """


                                                                     [35;1m1[0m        
                                                              \  | | | |      
North lane. (n,w,e)                                            [36;1mO[0m-[36;1mO[0m-[35;1m1[0m-[33;1m@[0m-[36;1mO[0m-[35;1m1[0m    
                                                               |   |   |      

[33mYou are on a street surfaced with weird, undulating green
tiles which goes from east to west.  The back of a building
lies to the south while an unprepossessing white building
stands doughtily to the north.
[0m
[33;1m    There are three obvious exits: north, west, east                       [0m
A tall street light.
> 

"""


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
        writePlugin("AreaMapper")
