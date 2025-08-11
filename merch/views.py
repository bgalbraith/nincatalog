from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Case, When, IntegerField, Value
from django.db.models.functions import Length

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


def search(request):
    query = request.GET.get('q', '').strip()
    results = []
    
    if query:
        # Create search filters for different fields
        search_filters = (
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(material__icontains=query) |
            Q(product_id__icontains=query) |
            Q(categories__name__icontains=query)
        )
        
        # Get products matching the search query, excluding unauthorized ones
        # Apply distinct after annotations to ensure unique results
        results = Product.objects.filter(search_filters).exclude(
            is_authorized='N'
        ).annotate(
            relevance_score=Case(
                # Exact match in name gets highest score
                When(name__iexact=query, then=Value(100)),
                # Name starts with query gets high score
                When(name__istartswith=query, then=Value(90)),
                # Name contains query gets medium-high score
                When(name__icontains=query, then=Value(80)),
                # Product ID match gets medium score
                When(product_id__icontains=query, then=Value(70)),
                # Material match gets medium score
                When(material__icontains=query, then=Value(60)),
                # Category name match gets lower score
                # causes duplicates, leaving for future investigation
                # When(categories__name__icontains=query, then=Value(50)),
                # Description match gets lowest score
                When(description__icontains=query, then=Value(40)),
                default=Value(0),
                output_field=IntegerField()
            )
        ).distinct().order_by('-relevance_score', 'name')
    
    return render(
        request,
        'merch/search_results.html',
        {
            'query': query,
            'results': results,
            'result_count': len(results)
        }
    )
