from django.shortcuts import render, get_object_or_404

from catalog.models import Category


def index(request):
    return render(request, 'catalog/index.html')


def category(request, category_tag):
    _category = get_object_or_404(Category, tag=category_tag)
    return render(request, 'catalog/category.html', {
        "category": _category
    })


def item(request, category_tag, item_tag):
    return render(request, 'catalog/item.html', {
        "category": category_tag,
        "item": item_tag
    })