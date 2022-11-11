from django.contrib import admin
from .models import Perfume, PerfumeBottle, Brand, Cart, CartProduct, Rating


admin.site.register(Perfume)
admin.site.register(PerfumeBottle)
admin.site.register(Brand)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Rating)
