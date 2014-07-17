from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ('name',)

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


class MediaPackage(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class MediaFormat(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=2)
    icon = models.ImageField(upload_to='countries')

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class MusicLabel(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
    icon = models.ImageField(upload_to='music_labels', null=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class Era(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    icon = models.ImageField(upload_to='eras')

    def __unicode__(self):
        return self.name


class Track(models.Model):
    related_tracks = models.ManyToManyField('self')
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class ItemRarity(models.Model):
    code = models.CharField(max_length=1)
    description = models.CharField(max_length=200)
    icon = models.ImageField(upload_to='rarity')
    scale_icon = models.ImageField(upload_to='rarity')

    def __unicode__(self):
        return self.code


class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist)
    category = models.ForeignKey(Category)
    media_format = models.ForeignKey(MediaFormat)
    media_package = models.ForeignKey(MediaPackage)
    media_notes = models.CharField(max_length=200)
    country = models.ForeignKey(Country)
    music_labels = models.ManyToManyField(MusicLabel)
    year = models.IntegerField()
    rarity = models.ForeignKey(ItemRarity)
    rarity_date = models.DateField(null=True, blank=True)
    era = models.ForeignKey(Era, null=True)
    notes = models.CharField(max_length=200)
    catalog_number = models.CharField(max_length=200)
    upc = models.CharField(max_length=200)
    discogs = models.IntegerField(null=True, blank=True)
    is_promo = models.BooleanField()
    is_authorized = models.BooleanField()
    release_date = models.DateField(null=True, blank=True)
    added_date = models.DateField(null=True, blank=True)
    old_key = models.CharField(max_length=8)

    class Meta:
        ordering = ('year', 'name', 'media_format', 'country',
                    'catalog_number')

    def __unicode__(self):
        return "%s (%s %s)" % (self.name, self.country.code,
                               self.media_format.name)


class ItemImageType(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class ItemImage(models.Model):
    image = models.ImageField(upload_to='item_images')
    item = models.ForeignKey(Item)
    type = models.ForeignKey(ItemImageType)

    class Meta:
        ordering = ('type',)


class Report(models.Model):
    name = models.CharField(max_length=200)
    tag = models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    field = models.CharField(max_length=200)
    icon = models.ImageField(upload_to='reports')
    n_columns = models.PositiveSmallIntegerField(default=3)
    column_width = models.PositiveSmallIntegerField(blank=True, null=True)

    def __unicode__(self):
        return self.name