from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200)
    tag = models.CharField(max_length=200)
    halo = models.PositiveSmallIntegerField(blank=True, null=True)
    icon = models.ImageField(upload_to='categories')

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
    icon = models.ImageField(upload_to='countries')

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


class ItemRarity(models.Model):
    code = models.CharField(max_length=1)
    icon = models.ImageField(upload_to='rarity')
    scale_icon = models.ImageField(upload_to='rarity')

    def __unicode__(self):
        return self.code


class Item(models.Model):
    category = models.ForeignKey(Category)
    artist = models.ForeignKey(Artist)
    format = models.ForeignKey(ItemFormat)
    country = models.ForeignKey(Country)
    label = models.ForeignKey(MusicLabel, null=True)
    rarity = models.ForeignKey(ItemRarity)

    name = models.CharField(max_length=200)
    year = models.IntegerField()
    notes = models.CharField(max_length=200)
    catalog_number = models.CharField(max_length=200)
    upc = models.CharField(max_length=200)
    packaging = models.CharField(max_length=200)
    release_date = models.DateField(null=True, blank=True)
    added_date = models.DateField()

    def __unicode__(self):
        return self.name