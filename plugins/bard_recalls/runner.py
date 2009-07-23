import urllib, urllib2
from urllib2 import URLError
import bard_parser

recall_file_path = "c:/Users/ckhrysze/Games/3k/bards/recall.txt"
f = open(recall_file_path, "r")

parser = bard_parser.FileParser()
entries = parser.parse(f)

for entry in entries:
    entry.submit()
