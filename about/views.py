from django.shortcuts import render
from django.http import HttpResponse

def about_us(request):
    return render(request, 'about/about.html')

def delivery_payment(request):
    return render(request, 'about/delivery_payment.html')
