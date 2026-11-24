from django.contrib import admin
from django.contrib.admin.options import ActionLocation
from model_clone import CloneModelAdmin

import catalog.models as models


class ItemImageInline(admin.TabularInline):
    model = models.ItemImage

class ItemTrackInline(admin.TabularInline):
    model = models.Track


class ItemAdmin(CloneModelAdmin):
    search_fields = ['name', 'artist__name']
    inlines = [
        ItemTrackInline,
        ItemImageInline
    ]
    # Registered the standard way rather than through django-clone's
    # _get_base_actions override; see below.
    actions = ['make_clone']

    def _get_base_actions(self, action_location=ActionLocation.CHANGE_LIST):
        # django-clone 5.5.0 overrides this private method without the
        # action_location argument Django 6.1 added, which makes every Item
        # admin page raise TypeError. Skip its override and use Django's.
        # Remove once django-clone supports 6.1.
        return admin.ModelAdmin._get_base_actions(self, action_location)


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
