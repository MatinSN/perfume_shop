from django.contrib import admin
from .models import Perfume, PerfumeBottle, Brand, Rating, Detail, Cart, CartProduct, PaymentsTrackId,PaidItem


admin.site.register(Perfume)
admin.site.register(PerfumeBottle)
admin.site.register(Brand)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Rating)
admin.site.register(Detail)
admin.site.register(PaymentsTrackId)
admin.site.register(PaidItem)

# admin.site.register(PaidProducts)
