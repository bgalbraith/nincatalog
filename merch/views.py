import random
import uuid

from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Case, When, IntegerField, Value
from django.db.models.functions import Length

from merch.models import Category, Product, ProductImage, Poster


def get_random_posters_for_session(request, shuffle=False):
    """Get posters in a consistent random order for this session"""
    # Ensure session exists
    if not request.session.session_key:
        request.session.create()
    
    if shuffle:
        request.session["seed"] = hash(uuid.uuid4())
    
    # Get all posters and convert to list for consistent ordering
    all_posters = list(Poster.objects.all())
    
    # Use the seed to randomize consistently
    random.seed(request.session.get("seed", 0))
    random.shuffle(all_posters)
    
    return all_posters


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


def posters(request):
    posters = get_random_posters_for_session(request, shuffle=True)
    return render(request, "merch/posters.html", {"posters": posters})


def poster_gallery(request, poster_id):
    clicked_poster = get_object_or_404(Poster, pk=poster_id)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Return JSON for AJAX requests with ALL posters in same random order as grid
        all_posters = get_random_posters_for_session(request)
        
        # Force caching of zoom specs
        for poster in all_posters:
            _ = poster.zoom.url
        
        # Find the index of the clicked poster
        try:
            initial_index = next(i for i, p in enumerate(all_posters) if p.id == clicked_poster.id)
        except StopIteration:
            initial_index = 0
        
        # Create poster data for all posters
        posters_data = []
        for poster in all_posters:
            posters_data.append({
                'id': poster.id,
                'url': poster.zoom.url,
                'submitter_name': poster.submitter_name
            })
        
        return JsonResponse({
            'posters': posters_data,
            'initial_index': initial_index
        })
    else:
        raise Http404

