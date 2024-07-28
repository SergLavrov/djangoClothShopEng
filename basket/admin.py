from django.contrib import admin
from basket.models import Basket, Delivery, Payment, Order, OrderItem

# Register your models here.

admin.site.register(Basket)
admin.site.register(Delivery)
admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(OrderItem)


