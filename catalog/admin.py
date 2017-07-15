from django.contrib import admin

import catalog.models as models


admin.site.register(models.Artist)
admin.site.register(models.Category)
admin.site.register(models.Country)
admin.site.register(models.Era)
admin.site.register(models.Item)
admin.site.register(models.ItemImage)
admin.site.register(models.ItemImageType)
admin.site.register(models.ItemRarity)
admin.site.register(models.MediaFormat)
admin.site.register(models.MediaPackage)
admin.site.register(models.MusicLabel)
admin.site.register(models.Report)
