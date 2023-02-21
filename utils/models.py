from django.db import models


class Color(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=7)

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=7)

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'State'
        verbose_name_plural = 'States'


class City(models.Model):
    name = models.CharField(max_length=30)
    state = models.ForeignKey(State, related_name='cities', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

# Create your models here.
