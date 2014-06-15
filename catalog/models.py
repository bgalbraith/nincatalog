from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200)
    tag = models.CharField(max_length=200)
    halo = models.PositiveSmallIntegerField(blank=True, null=True)

    def __unicode__(self):
        label = self.name
        if self.halo is not None:
            label = "%s (Halo %d)" % (label, self.halo)
        return label


class ItemFormat(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=2)

    def __unicode__(self):
        return self.name


class MusicLabel(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()

    def __unicode__(self):
        return self.name


class Track(models.Model):
    related_tracks = models.ManyToManyField('self')
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Item(models.Model):
    RARITY_CHOICES = (
        (0, 'S'), (1, 'A'), (2, 'B'), (3, 'C'), (4, 'D'), (5, 'E'), (6, 'N/A')
    )
    category = models.ForeignKey(Category)
    artist = models.ForeignKey(Artist)
    format = models.ForeignKey(ItemFormat)
    country = models.ForeignKey(Country)
    label = models.ForeignKey(MusicLabel, null=True)

    name = models.CharField(max_length=200)
    year = models.IntegerField()
    notes = models.CharField(max_length=200)
    catalog_number = models.CharField(max_length=200)
    upc = models.CharField(max_length=200)
    packaging = models.CharField(max_length=200)
    release_date = models.DateField(null=True, blank=True)
    added_date = models.DateField()
    rarity = models.IntegerField(choices=RARITY_CHOICES)

    def __unicode__(self):
        return self.name