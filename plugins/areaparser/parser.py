import re

class Area(object):
    def __init__(self, creators, name, realms):
        self.creators = creators
        self.name = name
        self.realms = realms

    def parse(lines):
        num = creators = name = realm = ""
        for line in lines:
            num += line[0:8]
            creators += line[8:28]
            name += line[29:64]
            realm += line[65:]
        area_creators = [creator.strip() for creator in creators.strip().split(" and ")]
        return Area(area_creators, name.strip(), realm.strip().split(" "))


    def __str__(self):
        return self.name
    def __repr__(self):
        return self.__str__()
