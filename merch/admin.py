from django.contrib import admin
from django.utils.text import slugify
from imagekit.admin import AdminThumbnail

import merch.models as models


def generate_tree_ids(parent=None, i=1):
    obs = []
    for c in models.Category.objects.filter(parent__exact=parent).order_by("order"):
        c.left_id = i
        children, j = generate_tree_ids(c, i+1)
        c.right_id = j
        obs.append(c)
        obs.extend(children)
        i = j + 1

    return obs, i


class CategoryAdmin(admin.ModelAdmin):
    exclude = ("left_id", "right_id", "tag")
    list_display = ["ascii_branch"]

    def ascii_branch(self, obj):
        depth = obj.depth()
        return ("--" * (depth - 1)) + " " + obj.name

    ascii_branch.short_description = "Category"

    def save_model(self, request, obj, form, change):
        obj.tag = slugify(obj.name)
        obj.save()
        objs, _ = generate_tree_ids()
        models.Category.objects.bulk_update(objs, ["left_id", "right_id"])

    def delete_model(self, request, obj):
        obj.product_set.clear()
        obj.delete()
        objs, _ = generate_tree_ids()
        models.Category.objects.bulk_update(objs, ["left_id", "right_id"])


class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    extra = 1
    readonly_fields = ["admin_thumbnail"]
    admin_thumbnail = AdminThumbnail(image_field="thumbnail_tiny")


class ProductAdmin(admin.ModelAdmin):
    search_fields = ["name", "categories__name"]
    ordering = ["name"]
    inlines = [
        ProductImageInline,
    ]


class OptionAdmin(admin.ModelAdmin):
    ordering = ["option_type__name", "name"]


class OptionTypeAdmin(admin.ModelAdmin):
    ordering = ["name"]


admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Option, OptionAdmin)
admin.site.register(models.OptionType, OptionTypeAdmin)
