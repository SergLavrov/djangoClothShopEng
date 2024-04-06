from django.urls import path
from . import views


urlpatterns = [
    path('about/', views.about_us, name='about'),
    path('delivery-payments/', views.delivery_payment, name='delivery_payment'),
]
