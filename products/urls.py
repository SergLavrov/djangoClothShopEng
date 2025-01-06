from django.urls import path
from . import views
from django.views.generic import RedirectView
from .views import ProductListView, ProductCategoryListView

urlpatterns = [
    path('', RedirectView.as_view(url='get-products/', permanent=True)),
    path('get-products/', ProductListView.as_view(), name='get-products'),
    # path('get-products/', views.get_products, name='get-products'),

    path('get-products-list/', views.get_products_list, name='get-products-list'),

    path('<int:product_id>/product-details/', views.product_details, name='product-details'),
    path('get-product-by-id/<int:product_id>/', views.get_product_by_id, name='get-product-by-id'),
    path('<int:product_id>/update-product/', views.update_product, name='update-product'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete-product'),
    path('add-product/', views.add_product, name='add-product'),

    path('search-product/', views.search_product, name='search-product'),

    path('search-list/', views.search_products_list, name='search-products-list'),
    # path('search-list/', ProductsFiltersListView.as_view(), name='search-products-list'),

    # path('get-products-category/<int:category_id>/', views.get_products_category, name='get-products-category'),
    path('get-products-category/<int:category_id>/', ProductCategoryListView.as_view(), name='get-products-category'),

    # path('get-clothing/', views.get_clothing, name='get-clothing'),
    # path('get-shoes/', views.get_shoes, name='get-shoes'),
    # path('get-accessories/', views.get_accessories, name='get-accessories'),
    # path('get-by-name-product/<str:product_name>/', views.get_by_name_product, name='get-by-name-product'),
    path('get-pants/', views.get_pants, name='get-pants'),
    path('get-jumpers/', views.get_jumpers, name='get-jumpers'),
    path('get-jeans/', views.get_jeans, name='get-jeans'),
    path('get-jackets/', views.get_jackets, name='get-jackets'),
    path('get-coats/', views.get_coats, name='get-coats'),
    path('get-shirts/', views.get_shirts, name='get-shirts'),
    path('get-tshirts/', views.get_tshirts, name='get-tshirts'),
    path('get-boots/', views.get_boots, name='get-boots'),
    path('get-sneakers/', views.get_sneakers, name='get-sneakers'),
    path('get-moccasins/', views.get_moccasins, name='get-moccasins'),
    path('get-list-shoes/', views.get_list_shoes, name='get-list-shoes'),
    path('get-ties/', views.get_ties, name='get-ties'),
    path('get-wallets/', views.get_wallets, name='get-wallets'),
    path('get-belts/', views.get_belts, name='get-belts'),
    path('get-bags/', views.get_bags, name='get-bags'),
    path('get-scavers/', views.get_scavers, name='get-scavers'),
 ]
