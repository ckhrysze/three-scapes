import urllib, urllib2
from urllib2 import URLError
import area_parser

f = open("all_areas.txt", "r")
buffer = f.readline().split("\r")
areas = area_parser.scan(buffer)

successes = 0

for area in areas:
    area.submit()
