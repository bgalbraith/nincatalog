from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse

import catalog.models as models


class ItemImageInline(admin.TabularInline):
    model = models.ItemImage

class ItemTrackInline(admin.TabularInline):
    model = models.Track


class ItemAdmin(admin.ModelAdmin):
    search_fields = ['name', 'artist__name']
    inlines = [
        ItemTrackInline,
        ItemImageInline
    ]
    actions = ['duplicate']

    @admin.action(
        description='Duplicate',
        description_plural='Duplicate selected items',
        permissions=['add'],
        location=[admin.ActionLocation.CHANGE_LIST, admin.ActionLocation.CHANGE_FORM],
    )
    def duplicate(self, request, queryset):
        copies = [item.duplicate() for item in queryset]
        if len(copies) == 1:
            self.message_user(request, f'Created a copy: {copies[0]}')
            return redirect(reverse('admin:catalog_item_change', args=[copies[0].pk]))
        self.message_user(request, f'Created {len(copies)} copies.')


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
