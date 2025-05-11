from django.db import models
from django.contrib.auth.models import User
from products.models import Product, SizeScale


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    same_items_price = models.FloatField(default=0)
    # size_prod = models.IntegerField()

    class Meta:
        ordering = ['created_timestamp']

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт {self.product.name_prod}'


class Delivery(models.Model):
    delivery_type = models.CharField(max_length=50)


class Payment(models.Model):
    payment_type = models.CharField(max_length=50)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    postcode = models.CharField(max_length=10)
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)
    # count_order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Заказ No{self.id}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
