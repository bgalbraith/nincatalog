from django.contrib import admin

from catalog.models import Artist, Category, MediaPackage, MediaFormat, \
    Country, MusicLabel, Era, ItemRarity, Item, ItemImage

admin.site.register(Artist)
admin.site.register(Category)
admin.site.register(MediaPackage)
admin.site.register(MediaFormat)
admin.site.register(Country)
admin.site.register(MusicLabel)
admin.site.register(Era)
admin.site.register(ItemRarity)
admin.site.register(Item)
admin.site.register(ItemImage)
