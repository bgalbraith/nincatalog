from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Category(models.Model):
    category = models.CharField(max_length=200)

    def __unicode__(self):
        return self.category