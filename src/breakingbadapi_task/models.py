from django.db import models


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
    character = models.ManyToManyField("Character")

    def __str__(self):
        return self.title
