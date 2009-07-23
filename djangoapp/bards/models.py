from django.db import models

class RecallEntry(models.Model):
    name = models.CharField(max_length=300)
    notes = models.TextField()
    links = models.CharField(max_length=300, blank=True)

    def fields(self):
        return ['name']

    class Meta:
        abstract = True

class AreaEntry(RecallEntry):
    coder = models.CharField(max_length=300, blank=True)
    realm = models.CharField(max_length=300, blank=True)
    level = models.CharField(max_length=300, blank=True)

    def fields(self):
        return [
            ('name', self.name),
            ('coder', self.coder),
            ('realm', self.realm),
            ('level', self.level),
            ]

class ArmourEntry(RecallEntry):
    type = models.CharField(max_length=300, blank=True)
    ac = models.CharField(max_length=300, blank=True)
    area = models.CharField(max_length=300, blank=True)
    mob = models.CharField(max_length=300, blank=True)
    unique = models.CharField(max_length=300, blank=True)
    special = models.CharField(max_length=300, blank=True)

    def fields(self):
        return [
            ('name', self.name),
            ('ac', self.ac),
            ('area', self.area),
            ('mob', self.mob),
            ('unique', self.unique),
            ('special', self.special),
            ]

class ItemEntry(RecallEntry):
    type = models.CharField(max_length=300, blank=True)
    area = models.CharField(max_length=300, blank=True)
    mob = models.CharField(max_length=300, blank=True)
    unique = models.CharField(max_length=300, blank=True)
    special = models.CharField(max_length=300, blank=True)

    def fields(self):
        return [
            ('name', self.name),
            ('area', self.area),
            ('mob', self.mob),
            ('unique', self.unique),
            ('special', self.special),
            ]

class MiscEntry(RecallEntry):
    def fields(self):
        return [
            ('name', self.name),
            ]

class MobEntry(RecallEntry):
    area = models.CharField(max_length=300, blank=True)
    mobClass = models.CharField(max_length=300, blank=True)
    special = models.CharField(max_length=300, blank=True)

    def fields(self):
        return [
            ('name', self.name),
            ('area', self.area),
            ('class', self.mobClass),
            ('special', self.special),
            ]

class WeaponEntry(RecallEntry):
    type = models.CharField(max_length=300, blank=True)
    wc = models.CharField(max_length=300, blank=True)
    area = models.CharField(max_length=300, blank=True)
    mob = models.CharField(max_length=300, blank=True)
    unique = models.CharField(max_length=300, blank=True)
    special = models.CharField(max_length=300, blank=True)

    def fields(self):
        return [
            ('name', self.name),
            ('wc', self.wc),
            ('area', self.area),
            ('mob', self.mob),
            ('unique', self.unique),
            ('special', self.special),
            ]
