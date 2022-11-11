
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
import datetime
import random

BRAND_CATEGORY_CHOICES = (
    ('LUX', 'LUX'),
    ('Designer', 'Designer')
)

GENDER_TYPES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Both', 'Both')
)


class Brand(models.Model):
    category = models.CharField(max_length=20, choices=BRAND_CATEGORY_CHOICES)
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='brands',
                              default='brands/aramis.png')

    def __str__(self):
        return self.name


class Perfume(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=1000)
    gender = models.CharField(max_length=10, choices=GENDER_TYPES)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='perfumes',
                              default='perfumes/p1.jpg')

    def __str__(self):
        return self.name


class PerfumeBottle(models.Model):
    perfume = models.ForeignKey(Perfume, on_delete=models.CASCADE)
    price = models.FloatField(default=round(random.uniform(
        1000000, 30000000), 2), validators=[MinValueValidator(1000000)])
    size = models.FloatField(default=round(random.uniform(100, 1000), 2),
                             validators=[MinValueValidator(100), MaxValueValidator(1000)])
    quantity = models.PositiveIntegerField(
        default=random.randint(100, 1000))
    discount = models.PositiveIntegerField(default=random.randint(10, 50))
    tester = models.BooleanField(default=False)
    rate = models.FloatField(default=round(random.uniform(0, 5), 2), validators=[
                             MinValueValidator(0), MaxValueValidator(5)])
    created_at = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.perfume.name


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Cart(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    products = models.ManyToManyField(
        PerfumeBottle,
        related_name='carts',
        through='CartProduct'
    )


class CartProduct(models.Model):
    product = models.ForeignKey(PerfumeBottle, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'cart'], name='unique_product_cart')
        ]


class Rating(models.Model):
    perfume = models.ForeignKey(PerfumeBottle, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    comment = models.CharField(max_length=500)
    created_at = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.user.username
