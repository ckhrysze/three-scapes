from django.db import models

class Wizard(models.Model):
    name = CharField(max_length=300)

class Realm(models.Model):
    name = CharField(max_length=300)

class Room(models.Model):
    title = models.CharField(max_length=300)
    desc = models.CharField(max_length=2000)

class Link(models.Model):
    name = models.CharField(max_length=300)
    obvious = models.BooleanField(default=True)
    length = models.IntegerField(default=54)
    start = models.ForeignKey(Room, related_name="exit_set")
    end = models.ForeignKey(Room, related_name="from_set", null=True)

class Map(models.Model):
    start = models.ForeignKey(Room)

class Area(models.Model):
    name = CharField(max_length=300)
    creators = ManyToManyField('Wizard')
    realms = ManyToManyField('Realm')
    rating = models.CharField(max_length=300)
    directions = models.CharField(max_length=300)
    areamap = models.ForeignKey(""
    defunct = BooleanField(default = False)
    closed = BooleanField(default = False)
