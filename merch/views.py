from django.http import Http404
from django.shortcuts import render, get_object_or_404

from merch.models import Category, Product, ProductImage


def index(request):
    categories = Category.objects.all()
    return render(request, "merch/index.html", {"categories": categories})


def category(request, category_tag):
    category = get_object_or_404(Category, tag=category_tag)
    products = filter(lambda p: p.is_authorized != "N", category.products())
    return render(  
        request,
        "merch/category.html",
        {"category": category, "products": products},
    )


def product(request, category_tag, product_tag):
    category = get_object_or_404(Category, tag=category_tag)
    pk = product_tag.split("-")[-1]
    product = get_object_or_404(Product, pk=pk)

    if category not in product.deep_categories():
        raise Http404
    
    images = product.productimage_set.all()
    # force caching of zoom spec if needed
    for image in images:
        _ = image.zoom.url
    return render(
        request,
        "merch/product.html",
        {"category": category, "product": product, "images": images},
    )
