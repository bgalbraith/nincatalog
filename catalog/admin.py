from django.contrib import admin

import catalog.models as models


class ItemImageInline(admin.TabularInline):
    model = models.ItemImage


class ItemAdmin(admin.ModelAdmin):
    inlines = [
        ItemImageInline
    ]


admin.site.register(models.Artist)
admin.site.register(models.Category)
admin.site.register(models.Country)
admin.site.register(models.Era)
admin.site.register(models.Item, ItemAdmin)
admin.site.register(models.ItemImage)
admin.site.register(models.ItemImageType)
admin.site.register(models.ItemRarity)
admin.site.register(models.MediaFormat)
admin.site.register(models.MediaPackage)
admin.site.register(models.MusicLabel)
admin.site.register(models.Report)
