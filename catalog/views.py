from django.shortcuts import render


def index(request):
    return render(request, 'catalog/index.html')


def category(request, category_tag):
    return render(request, 'catalog/category.html', {
        "category": category_tag
    })


def item(request, category_tag, item_tag):
    return render(request, 'catalog/item.html', {
        "category": category_tag,
        "item": item_tag
    })