from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.db.models import Count

from catalog.models import Artist, Category, Country, Era, Item, MediaFormat, \
    MediaPackage, MusicLabel, Report


def index(request):
    _halo_group = Category.objects.filter(halo__isnull=False)
    _other_group = Category.objects.filter(halo__isnull=True) \
        .annotate(n_item=Count('item')).filter(n_item__gt=0)
    _report_group = Report.objects.all()
    return render(request, 'catalog/index.html', {
        "halo_group": _halo_group,
        "other_group": _other_group,
        "report_group": _report_group
    })


def category(request, category_tag):
    _category = get_object_or_404(Category, tag=category_tag)
    _group = header_group(_category.halo is not None)
    _items = _category.item_set.all()
    _listing = {
        'title': _category.name.lower(),
        'selected': _category,
        'categories': [
            {
                'name': _category.name,
                'halo': _category.halo,
                'tag': _category.tag,
                'items': _items
            }
        ]
    }
    return render(request, 'catalog/listing.html', {
        "listing": _listing,
        "group": _group
    })


def item(request, category_tag, item_tag):
    _category = get_object_or_404(Category, tag=category_tag)
    _item = get_object_or_404(Item, pk=item_tag)
    if _category != _item.category:
        raise Http404

    _group = header_group(_category.halo is not None)
    return render(request, 'catalog/item.html', {
        "category": _category,
        "group": _group,
        "item": _item
    })


def report(request, report_tag):
    _report = get_object_or_404(Report, tag=report_tag)
    model = globals().get(_report.model, None)
    if model is None:
        raise Http404

    _entries = model.objects.annotate(n_items=Count('item')) \
        .filter(n_items__gt=0)
    col_length = len(_entries) / _report.n_columns
    if len(_entries) % _report.n_columns != 0:
        col_length += 1
    _entries = [_entries[i::col_length] for i in range(col_length)]
    _group = header_group(False)
    return render(request, 'catalog/report.html', {
        "report": _report,
        "entries": _entries,
        "group": _group
    })


def report_details(request, report_tag, entry_tag):
    _report = get_object_or_404(Report, tag=report_tag)
    _model = globals().get(_report.model, None)
    if _model is None:
        raise Http404
    _entry = get_object_or_404(_model, pk=entry_tag)
    _categories = list()
    for _category in Category.objects.all():
        filter_kwargs = {'category': _category.pk, _report.field: _entry.pk}
        _items = Item.objects.filter(**filter_kwargs)
        if _items.count() > 0:
            _categories.append({
                'name': "%s / %s" % (_entry.name, _category.name),
                'halo': _category.halo,
                'tag': _category.tag,
                'items': _items
            })
    _listing = {
        'title': '%s - %s' % (_report.name.lower(), _entry.name.lower()),
        'selected': _report,
        'categories': _categories
    }
    _group = header_group(False)
    return render(request, 'catalog/listing.html', {
        "listing": _listing,
        "group": _group
    })


def header_group(is_halo):
    if is_halo:
        group = {'categories': Category.objects.filter(halo__isnull=False)}
    else:
        categories = Category.objects.filter(halo__isnull=True) \
            .annotate(n_item=Count('item')).filter(n_item__gt=0)
        reports = Report.objects.all()
        group = {'categories': categories, 'reports': reports}
    return group


def handle404(request):
    response = render(request, 'catalog/404.html', {})
    response.status_code = 404
    return response
