from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class ItemFormat(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name