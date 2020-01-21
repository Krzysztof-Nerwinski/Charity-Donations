from django.core.validators import MinValueValidator
from django.db.models import Min

from accounts.models import CustomUser
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Institution(models.Model):
    types = (
        (1, 'Fundacja'),
        (2, 'Organizacja pozarządowa'),
        (3, 'Zbiórka lokalna')
    )
    name = models.CharField(max_length=256)
    description = models.TextField(null=True)
    type = models.IntegerField(choices=types, default=1)
    categories = models.ManyToManyField(Category)


class Donation(models.Model):
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT)
    address = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=15)
    city = models.CharField(max_length=64)
    zip_code = models.CharField(max_length=10)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField(blank=True)
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)
