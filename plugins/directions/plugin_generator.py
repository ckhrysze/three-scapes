import re

class Directions(object):
    def __init__(self):
        self.direction_map = [
            ("epic", "12n (leave/enter) 8n 4e 6n 4w 3n (enter)", BasicNavigator),
            ("catacombs", "12n (leave/enter) 8n 3e 7n w d", BasicNavigator),
            ("lonely_keep", "12n (leave/enter) 8n 4e 6n 4w n (enter)", BasicNavigator),
            ("arcanarton", "12n (leave/enter) 8n 4e 6n 11w s (sw) (trail)", BasicNavigator),
            ("grindur", "12n (leave/enter) 8n 4e 6n 11w n (enter)", BasicNavigator),
            ("giant_camp", "12n (leave/enter) 8n 4e 6n 12w (enter)", BasicNavigator),
            ("mage_tower", "12n (leave/enter) 8n 4e 6n 4w n 7e (enter)", BasicNavigator),
            ("balooga_falls", "12n (leave/enter) 8n 4e 6n 13w (enter)", BasicNavigator),
            ("rimalkin_cave", "12n (leave/enter) 8n 4e 6n 7w s (enter", BasicNavigator),
            ("kazhirs_hut", "12n (leave/enter) 8n 4e 6n 4w n 12e (enter)", BasicNavigator),
            ("road_portal", "12n (leave/enter) 8n 4e 6n 9w", BasicNavigator),
            ("dragon_lair", "12n (leave/enter) 8n 4e 6n 9w 2s (enter)", BasicNavigator),
            ]
        self.re_to = re.compile("_to_(\w+)")
        self.re_reverse = re.compile("_(?:reverse|from)_(\w+)")
        self.re_show = re.compile("_show_(\w+)")


    def on_command_entered(self, cmd):
        found = False
        match = self.re_to.search(cmd)
        if match: found = self.search_and_execute_directions(match.group(1))

        match = self.re_reverse.search(cmd)
        if match: found = self.search_and_execute_directions(match.group(1), True)

        match = self.re_show.search(cmd)
        if match: found = self.search_directions(match.group(1), True)

        return found

    def search_and_execute_directions(self, location, reverse = False):
        for name, dirs, nav_class in self.direction_map:
            if location == name:
                nav = nav_class()
                nav.execute(dirs, reverse)
                return True
        return False

    def search_directions(self, location, reverse = False):
        for name, dirs, nav_class in self.direction_map:
            if location == name:
                world.Note(dirs)
                return True
        return False

class MidwayNavigator(object):
    def __init__(self): pass
    def execute(self, dirs, reverse):
        world.Execute("brief on no")
        if reverse: world.ReverseSpeedwalk(dirs)
        else: world.EvaluateSpeedwalk(dirs)
        world.Execute("brief off yes")
        world.Execute("look")

class BasicNavigator(object):
    def __init__(self): pass
    def execute(self, dirs, reverse):
        world.Execute("brief on no")
        if reverse:
            world.send( world.ReverseSpeedwalk(dirs) )
        else:
            world.send( world.EvaluateSpeedwalk(dirs) )
        world.Execute("brief off yes")
        world.Execute("look")

directions = Directions()

def OnPluginCommandEntered(cmd):
    global directions
    if directions.on_command_entered(cmd): return "\t"
    return cmd

