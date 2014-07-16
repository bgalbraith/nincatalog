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
    _group = Category.objects.filter(halo__isnull=_category.halo is None) \
        .annotate(n_item=Count('item')).filter(n_item__gt=0)
    return render(request, 'catalog/category.html', {
        "category": _category,
        "group": _group
    })


def item(request, category_tag, item_tag):
    _category = get_object_or_404(Category, tag=category_tag)
    _item = get_object_or_404(Item, pk=item_tag)
    if _category == _item.category:
        _group = Category.objects.filter(halo__isnull=_category.halo is None) \
            .annotate(n_item=Count('item')).filter(n_item__gt=0)
        return render(request, 'catalog/item.html', {
            "category": _category,
            "group": _group,
            "item": _item
        })
    else:
        raise Http404


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
    _group = Category.objects.filter(halo__isnull=True) \
        .annotate(n_item=Count('item')).filter(n_item__gt=0)
    return render(request, 'catalog/report.html', {
        "report": _report,
        "entries": _entries,
        "group": _group
    })