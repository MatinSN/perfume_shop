
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Brand(models.Model):
    category = models.CharField(max_length=100)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Perfume(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    price = models.FloatField()
    size = models.FloatField()
    sex = models.CharField(max_length=30)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class PerfumeBottle(models.Model):
    perfume = models.ForeignKey(Perfume, on_delete=models.CASCADE)
    price = models.FloatField()
    size = models.FloatField()
    quantity = models.IntegerField()
    tester = models.BooleanField(default=False)

    def __str__(self):
        return self.perfume.name


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# class MenPerfume(models.Model):
#     info = models.ForeignKey(PerfumeInfo, on_delete=models.PROTECT)
#     price = models.FloatField()
#     size = models.FloatField()

#     def __str__(self):
#         return self.info.name
