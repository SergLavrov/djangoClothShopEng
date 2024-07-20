from django.db import models


class Company(models.Model):                        # КОМПАНИИ/ПРОДАВЦЫ
    name_company = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)

    class Meta:
        ordering = ['name_company']


class Category(models.Model):                       # КАТЕГОРИИ ТОВАРОВ (ОДЕЖДА, ОБУВЬ, АКСЕССУАРЫ)
    name_category = models.CharField(max_length=50)


class Season(models.Model):
    name_season = models.CharField(max_length=50)


class ProductComposition(models.Model):                         # СОСТАВ ТОВАРА
    product_composition = models.CharField(max_length=50)


class SizeScale(models.Model):
    size_scale = models.IntegerField()


class Product(models.Model):
    name_prod = models.CharField(max_length=50)
    article = models.CharField(max_length=50)
    description = models.TextField(null=True)
    color = models.CharField(max_length=50)
    price = models.FloatField()
    product_count = models.IntegerField()  # (наличие товара на складе, единиц)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    season = models.ForeignKey(Season, on_delete=models.SET_NULL, null=True)
    product_composition = models.ForeignKey(ProductComposition, on_delete=models.SET_NULL, null=True)
    size_scale = models.ForeignKey(SizeScale, on_delete=models.SET_NULL, null=True, default=0)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    image = models.ImageField('/product_image/')
    is_deleted = models.BooleanField(default=False)
    # file = models.FileField('car_file/')  # можно прикрепить ещё файл (например doc, txt и т.д.)
    # image = models.ImageField(upload_to='/products_images', blank=True)          # (ФОТО товара)

    class Meta:
        ordering = ['id']
    #     ordering = ['name']

