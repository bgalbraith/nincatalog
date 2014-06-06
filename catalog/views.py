from django.shortcuts import render


def index(request):
    return render(request, 'catalog/index.html')


def category(request, category):

    return render(request, 'catalog/category.html', {
        "category": category
    })