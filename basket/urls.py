from django.urls import path
from . import views


urlpatterns = [
    path('in-basket/', views.in_basket, name='in-basket'),
    # path('in-basket2/<int:item_id>/', views.in_basket2, name='in-basket2'),
    path('add/<int:product_id>/', views.add_to_basket, name='add-to-basket'),

    # path('add/<int:product_id>/<int:size_select_id>/', views.add_to_basket, name='add-to-basket'),
    # path('select-size/<int:product_id>/', views.select_size, name='select-size'),

    # path('change/<int:item_id>/', views.change_qty, name='change-qty'),
    path('change-plus-minus/<int:item_id>/', views.change_qty_plus_minus, name='change-qty-plus-minus'),

    path('delete/<int:item_id>/', views.delete_from_basket, name='delete-from-basket'),
    path('no-product-in-stock/', views.no_product_in_stock, name='no-product-in-stock'),
    path('create-order/', views.create_order, name='create-order'),
    path('order-list/', views.order_list, name='order-list'),
    path('is-processed/<int:order_id>/', views.is_processed, name='is-processed'),
    path('delete-order/<int:order_id>/', views.delete_order, name='delete-order'),
]
