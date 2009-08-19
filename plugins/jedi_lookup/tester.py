import unittest
from mock import Mock
import __builtin__
__builtin__.world = Mock()

import plugin_generator

#<areas/monsters/armours/weapons/items/reviews/misc>
class PluginGeneratorTest(unittest.TestCase):

    def testMiscList(self):
        plugin_generator.OnPluginPacketReceived(packet)
        self.assertEquals(
            world.method_calls,
            [
                ('send', ('focus lookup on Guild_Terminology',), {}),
                ('send', ('focus lookup on intell_boost',), {}),
                ('send', ('focus lookup on star_wars',), {}),

                ('send', ('focus lookup on Newbie_Jedi_Info',), {}),
                ('send', ('focus lookup on money',), {}),
                ('send', ('focus lookup on stat_boosts',), {}),

                ('send', ('focus lookup on alignment_pool',), {}),
                ('send', ('focus lookup on money_making',), {}),
                ('send', ('focus lookup on telnet',), {}),

                ('send', ('focus lookup on being_a_new_jedi',), {}),
                ('send', ('focus lookup on mud_damage_emotes',), {}),
                ('send', ('focus lookup on test',), {}),

                ('send', ('focus lookup on cha_scroll',), {}),
                ('send', ('focus lookup on newbie_faq_by_moose',), {}),
                ('send', ('focus lookup on webpage',), {}),

                ('send', ('focus lookup on dark_jedi_tipe',), {}),
                ('send', ('focus lookup on overmax_sp',), {}),
                ('send', ('focus lookup on webpages',), {}),
                ]
            )

packet = """
Jedi Archive Contents for: misc
Guild_Terminology       intell_boost            star_wars
Newbie_Jedi_Info        money                   stat_boosts
alignment_pool          money_making            telnet
being_a_new_jedi        mud_damage_emotes       test
cha_scroll              newbie_faq_by_moose     webpage
dark_jedi_tipe          overmax_sp              webpages

> 
"""

packet2 = """
 ------------------------------------------------
| Name: Easy Intell stat Boost                   |
 ------------------------------------------------
| Realm: Chaos                                   |
 ------------------------------------------------
| Area: Ice Fishing                              |
 ------------------------------------------------

Gehn's comments: (Tue Apr 18 12:36:50 2000)
An easyish +1 intell stat boost is found in Igor's Ice Fishing 
area of Chaos. The boost lasts for login. To get there from 
the vortex: 3e/2s/2e/n/2e/2s/sw/w/open door/w. Kill the 
fisherman (aprox 2.5K) get all and wield pole.  Then: 
door/e/ne/open door/w. Type 'fish' repeatedly until you see a 
message about brain food. This can take some time so be 
patient. Also watch your HP's, as there are electric catfish 
that will bite on occasion.
"""

def writePlugin(name):
    from jinja2 import FileSystemLoader, Template, Environment

    plugin_dir = "C:/Program Files (x86)/MUSHclient/worlds/plugins/"

    loader = FileSystemLoader("templates")
    env = Environment(loader=loader)
    template = env.get_template("%s.xml" % (name))

    plugin_source = open("plugin_generator.py", "r")
    lines = []
    for line in plugin_source.readlines():
        lines.append(line)
    plugin_output = open("%s/%s.xml" % (plugin_dir, name), "w")
    plugin_output.write(template.render(py_script=lines))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(PluginGeneratorTest)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        print "Errors found, plugin not generated"
    else:
        writePlugin("JediLookup")
