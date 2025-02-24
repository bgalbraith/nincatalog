from itertools import chain

from django.db import models
from django.utils.text import slugify
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Category(models.Model):
    parent = models.ForeignKey(
        "Category", null=True, blank=True, on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)
    tag = models.CharField(max_length=200)
    left_id = models.IntegerField(default=0)
    right_id = models.IntegerField(default=0)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["left_id"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def products(self):
        """
        Returns a flat list of all products that fall within a category and
        its children.
        """
        children = Category.objects.filter(
            left_id__gt=self.left_id, right_id__lt=self.right_id
        )
        products = [self.product_set.all()]
        for child in children:
            products.append(child.product_set.all())

        return set(chain.from_iterable(products))

    def depth(self):
        """
        Returns the depth of a category in the category hierarchy.
        """
        depth = 1
        parent = self.parent
        while parent is not None:
            depth += 1
            parent = parent.parent

        return depth

    def family(self):
        """
        Returns a flat list of the immediate children, siblings, and ancestors
        of a category.
        """
        # add children
        family = list(Category.objects.filter(parent__exact=self))
        if self.parent is None:
            family += list(Category.objects.filter(parent__exact=None))
        else:
            parent = self.parent
            while parent is not None:
                # add siblings
                family += list(Category.objects.filter(parent__exact=parent))
                # add parent
                family.append(parent)
                parent = parent.parent

        return set(family)


class OptionType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Option(models.Model):
    option_type = models.ForeignKey(OptionType, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    abbreviation = models.CharField(max_length=10)

    def __str__(self):
        return "[%s] %s" % (self.option_type.name, self.name)

    def type(self):
        return self.option_type.name


class Product(models.Model):
    categories = models.ManyToManyField(Category)
    name = models.CharField(max_length=200)
    description = models.TextField()
    options = models.ManyToManyField(Option)

    def __str__(self):
        return self.name

    def tag(self):
        return slugify("-".join([self.name, str(self.id)]))

    def deep_categories(self):
        """
        Returns a flat list of all the product's categories and ancestors.
        """
        categories = list(self.categories.all())
        for category in self.categories.all():
            parent = category.parent
            while parent:
                categories.append(parent)
                parent = parent.parent

        return categories


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    original = models.ImageField(upload_to="product_images")
    zoom = ImageSpecField(
        source="original", processors=[ResizeToFill(500, 500)], format="PNG"
    )
    thumbnail = ImageSpecField(
        source="original", processors=[ResizeToFill(200, 200)], format="PNG"
    )
    thumbnail_medium = ImageSpecField(
        source="original", processors=[ResizeToFill(100, 100)], format="PNG"
    )
    thumbnail_tiny = ImageSpecField(
        source="original", processors=[ResizeToFill(50, 50)], format="PNG"
    )
    order = models.SmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return "%s [%d]" % (self.product.name, self.order)
