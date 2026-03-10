from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Type(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Ability(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Move(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Pokemon(models.Model):
    name = models.CharField(max_length=100, unique=True)

    height = models.IntegerField()
    weight = models.IntegerField()

    types = models.ManyToManyField(Type)
    abilities = models.ManyToManyField(Ability)
    moves = models.ManyToManyField(Move)

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']