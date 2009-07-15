import unittest
import area_parser

class ParserTest(unittest.TestCase):

    def testBasicParsing(self):
        lines = [
            "   1.   Adalius              B Sharp Jazz Club                   Chaos       ",
        ]
        area = area_parser.parse(lines)
        self.assertEquals("B Sharp Jazz Club", area.name)
        self.assertEquals(["Adalius"], area.creators)
        self.assertEquals(["Chaos"], area.realms)

    def testDualCreator(self):
        lines = [
            "   6.   Alfonzo and          Alfonzo's Nightmare                 Chaos",
            "        Tuesdai           ",
            ]
        area = area_parser.parse(lines)
        self.assertEquals("Alfonzo's Nightmare", area.name)
        self.assertEquals(['Alfonzo', 'Tuesdai'], area.creators)
        self.assertEquals(["Chaos"], area.realms)

    def testThreeCreators(self):
        lines = [
            " 408.   Samiel, Heroin and   Old London                          Chaos",
            "        Crowley",
            ]
        area = area_parser.parse(lines)
        self.assertEquals("Old London", area.name)
        self.assertEquals(['Samiel', 'Heroin', 'Crowley'], area.creators)
        self.assertEquals(["Chaos"], area.realms)

    def testClosedRealm(self):
        lines = [
            "  42.   Blizzard             Halloween Shop                      Pinnacle",
            "                                                                 (CLOSED)    ",
            ]
        area = area_parser.parse(lines)
        self.assertEquals("Halloween Shop", area.name)
        self.assertEquals(['Blizzard'], area.creators)
        self.assertEquals(["Pinnacle"], area.realms)
        self.assertTrue(area.is_closed)

    def testDefunctRealm(self):
        lines = [
            "  52.   Briareos             Arendia                             Fantasy",
            "                                                                 (DEFUNCT)   ",
            ]
        area = area_parser.parse(lines)
        self.assertEquals("Arendia", area.name)
        self.assertEquals(['Briareos'], area.creators)
        self.assertEquals(["Fantasy"], area.realms)
        self.assertTrue(area.is_defunct)

    def testMultiRealm(self):
        lines = [
            " 118.   Dynon                Codename:Kodiak                     Science and",
            "                                                                 Newbieland  ",
            ]
        area = area_parser.parse(lines)
        self.assertEquals("Codename:Kodiak", area.name)
        self.assertEquals(['Dynon'], area.creators)
        self.assertEquals(["Science", "Newbieland"], area.realms)

    def testScan(self):
        areas = area_parser.scan(small_area_list.split("\n"))
        self.assertEquals(43, len(areas))

small_area_list = """
                            Areas of 3 Kingdoms
                             (651 areas listed)
 No.:   Creator(s):          Area Name:                          Realm:
 ----   -----------          ----------                          ------
   5.   Alerik               O'Hare International Airport        Science
   6.   Alfonzo and          Alfonzo's Nightmare                 Chaos
        Tuesdai
   7.   Amish                Halo                                Chaos
  23.   Aserena              Waldo's House                       Chaos
  24.   Aserena and          Electric Cave                       Chaos
        Frizzle
  25.   Asheratyluk          Aruwin's Windmill                   Fantasy
  38.   Blackstaff and       Hobgoblin Cave                      Fantasy
        Pull
  42.   Blizzard             Halloween Shop                      Pinnacle
                                                                 (CLOSED)
  52.   Briareos             Arendia                             Fantasy
                                                                 (DEFUNCT)
  53.   Briareos             Pandaemonium                        Chaos
  70.   Cirrus               Sea Cliffs                          Fantasy
More: 0-79(694) : [q,b,<cr>]
  71.   Cirrus               Seahaven                            Fantasy
  73.   Cletus               D.C. Megatech                       Science
  74.   Cletus               First Church of Christ, Computer    Science
                             Programmer
  79.   Crolack              X1S17 Stealth Tank                  Science
 106.   Doh and Lostar       The Simpsons                        Chaos
 107.   Dozy                 Desert Caverns                      Fantasy
 116.   Druss and Darkfyre   Arovian Graveyard                   Fantasy
 118.   Dynon                Codename:Kodiak                     Science and
                                                                 Newbieland
 119.   Dynon                Newbieland Transportation Center    Newbieland
                                                                 (DEFUNCT)
 133.   Fido                 Goon Shop                           Pinnacle
                                                                 (DEFUNCT)
 144.   Ganzie               Clear Falls Valley                  Fantasy
More: 80-159(694) [q,b,<cr>]
 174.   Horus                Warhammer 40,000                    Science
 178.   Igor and Edroman     WWF Ring                            Chaos
 200.   Kendric              3Kraft                              Chaos
 201.   Kendric              Dead or Alive 3                     Chaos
 202.   Kendric              Diablo II                           Chaos
 206.   Kinslayer            3-Kingdoms Explorer's Inn           Pinnacle
 213.   Kintax               R'lyeh                              Chaos
 220.   Kohl and Sioux       Game Show                           Chaos
More: 160-239(694) [q,b,<cr>]
 408.   Samiel, Heroin and   Old London                          Chaos
        Crowley
 471.   Stelari and Casso    Cowville                            Chaos
 480.   Syd and Arrion       Walled Lake Central High School     Chaos
 557.   Tiro and             Wayhaven                            Fantasy
        Blackstaff
 558.   Tiro and Cletus      Pinnacle                            Pinnacle
 559.   Tiro and Zetron      Isle of Kimlark                     Fantasy
 560.   To                   A Dark Cavern                       Fantasy
 561.   Toad                 Bots 'R' Us                         Science
 565.   Tramane, Thyros      Crevice of the Mystic Seal          Fantasy
        and Kendric
 658.   Zix                  Wayhaven Arena                      Fantasy
 659.   Zoom                 Smurfland                           Chaos
>
"""

if __name__ == '__main__':
    unittest.main()
