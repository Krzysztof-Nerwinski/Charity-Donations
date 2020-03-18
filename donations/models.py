from django.core.validators import MinValueValidator
from accounts.models import CustomUser
from django.db import models

FOUNDATION = 1
ORGANIZATION = 2
LOCAL_COLLECTION = 3


class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name='Nazwa')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Kategoria'
        verbose_name_plural = 'Kategorie'


class Institution(models.Model):

    types = (
        (FOUNDATION, 'Fundacja'),
        (ORGANIZATION, 'Organizacja pozarządowa'),
        (LOCAL_COLLECTION, 'Zbiórka lokalna')
    )

    name = models.CharField(max_length=256, verbose_name='Nazwa')
    description = models.TextField(null=True, verbose_name='Opis')
    type = models.IntegerField(choices=types, default=FOUNDATION)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Instytucja'
        verbose_name_plural = 'Instytucje'


class Donation(models.Model):
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name='Worki')
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT, verbose_name='Instytucja')
    address = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=15)
    city = models.CharField(max_length=64)
    zip_code = models.CharField(max_length=10)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField(blank=True)
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL, verbose_name='Użytkownik')
    is_taken = models.BooleanField(default=False, verbose_name="Zrealizowane")

    class Meta:
        verbose_name = 'Darowizna'
        verbose_name_plural = 'Darowizny'
