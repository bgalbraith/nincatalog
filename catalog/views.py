from django.http import Http404
from django.shortcuts import render, get_object_or_404

from catalog.models import Category, Item


def index(request):
    _group = Category.objects.filter(halo__gt=0)
    return render(request, 'catalog/index.html', {
        "group": _group
    })


def category(request, category_tag):
    _category = get_object_or_404(Category, tag=category_tag)
    _group = Category.objects.filter(halo__isnull=_category.halo is None)
    return render(request, 'catalog/category.html', {
        "category": _category,
        "group": _group
    })


def item(request, category_tag, item_tag):
    _category = get_object_or_404(Category, tag=category_tag)
    _item = get_object_or_404(Item, pk=item_tag)
    if _category == _item.category:
        _group = Category.objects.filter(halo__gt=0)
        return render(request, 'catalog/item.html', {
            "category": _category,
            "group": _group,
            "item": _item
        })
    else:
        raise Http404