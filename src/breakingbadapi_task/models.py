from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point
from django.db import models
from django.utils import timezone


class Character(models.Model):
    STATUS_CHOICES = (
        ("Presumed dead", "Presumed dead"),
        ("Alive", "Alive"),
        ("Deceased", "Deceased"),
        ("Unknown", "Unknown"),
    )

    name = models.CharField(max_length=70)
    birthday = models.DateField(null=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=13)

    def __str__(self):
        return self.name


class Occupation(models.Model):
    title = models.CharField(max_length=70)
    character = models.ManyToManyField("Character", related_name="occupation")

    def __str__(self):
        return self.title


def now():
    """Wrapper which allows to monkey patch timezone.now() in tests"""
    return timezone.now()


class Location(models.Model):

    character = models.ForeignKey("Character", related_name="locations", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=now, null=False, blank=False)
    point = gis_models.PointField(default=Point(0, 0))

    def __str__(self):
        return f"{self.character.name} {self.timestamp} {self.point.x}:{self.point.y}"
