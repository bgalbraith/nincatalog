from django.db import models
from django.utils.text import slugify
from model_clone import CloneMixin


class Artist(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200)
    tag = models.CharField(max_length=200)
    halo = models.PositiveSmallIntegerField(blank=True, null=True)
    icon = models.ImageField(upload_to='categories')

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        label = self.name
        if self.halo is not None:
            label = "%s (Halo %d)" % (label, self.halo)
        return label


class MediaPackage(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Media Packages'

    def __str__(self):
        return self.name


class MediaFormat(models.Model):
    name = models.CharField(max_length=200)
    tag = models.CharField(max_length=200, default='')

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Media Formats'

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=2)
    icon = models.ImageField(upload_to='countries')

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name


class MusicLabel(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
    icon = models.ImageField(upload_to='music_labels', null=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Music Labels'

    def __str__(self):
        return self.name


class Era(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    icon = models.ImageField(upload_to='eras')

    def __str__(self):
        return self.name


class Track(models.Model):
    related_tracks = models.ManyToManyField('self')
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class ItemRarity(models.Model):
    code = models.CharField(max_length=1)
    description = models.CharField(max_length=200)
    icon = models.ImageField(upload_to='rarity')
    scale_icon = models.ImageField(upload_to='rarity')

    class Meta:
        ordering = ('id',)
        verbose_name_plural = 'Item Rarities'

    def __str__(self):
        return self.code


class Item(CloneMixin, models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    media_format = models.ForeignKey(MediaFormat, on_delete=models.CASCADE)
    media_package = models.ForeignKey(MediaPackage, on_delete=models.CASCADE)
    media_notes = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    music_labels = models.ManyToManyField(MusicLabel)
    year = models.IntegerField()
    rarity = models.ForeignKey(ItemRarity, on_delete=models.CASCADE)
    rarity_date = models.DateField(null=True, blank=True)
    era = models.ForeignKey(Era, null=True, on_delete=models.CASCADE)
    notes = models.TextField()
    catalog_number = models.CharField(max_length=200)
    upc = models.CharField(max_length=200)
    discogs = models.IntegerField(null=True, blank=True)
    is_promo = models.BooleanField(default=False)
    is_authorized = models.BooleanField(default=False)
    release_date = models.DateField(null=True, blank=True)
    added_date = models.DateField(null=True, blank=True)
    old_key = models.CharField(max_length=8, null=True, blank=True)

    _clone_m2m_fields = ['music_labels']

    class Meta:
        ordering = ('year', 'release_date', 'name', 'media_format', 'country',
                    'catalog_number')

    def __str__(self):
        return "%s (%s %s)" % (self.name, self.country.code,
                               self.media_format.name)

    def tag(self):
        return slugify("-".join([self.name,
                                 self.country.code,
                                 self.media_format.tag,
                                 str(self.id)]))


class ItemImageType(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Item Image Types'

    def __str__(self):
        return self.name


class ItemImage(models.Model):
    image = models.ImageField(upload_to='item_images')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    type = models.ForeignKey(ItemImageType, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ('order',)
        verbose_name_plural = 'Item Images'

    def __str__(self):
        return "%s [%s]" % (self.item, self.type)


class Report(models.Model):
    name = models.CharField(max_length=200)
    tag = models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    field = models.CharField(max_length=200)
    icon = models.ImageField(upload_to='reports')
    n_columns = models.PositiveSmallIntegerField(default=3)
    column_width = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return self.name
