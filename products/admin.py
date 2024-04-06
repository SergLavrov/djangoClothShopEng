from django.contrib import admin
from .models import Company, Category, Season, ProductComposition, SizeScale, Product
from django.contrib.auth.models import Permission

# Register your models here.

admin.site.register(Company)
admin.site.register(Category)
admin.site.register(Season)
admin.site.register(ProductComposition)
admin.site.register(SizeScale)
admin.site.register(Product)
admin.site.register(Permission)

