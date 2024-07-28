from django.urls import path
from . import views


urlpatterns = [
    path('create/', views.create_ticket, name='create-ticket'),
    path('ticket-list', views.ticket_list, name='ticket-list'),
    path('ticket-reviews', views.ticket_reviews, name='ticket-reviews'),
    path('<int:ticket_id>/ticket-detail', views.ticket_detail, name='ticket-detail'),
    path('<int:ticket_id>/delete-ticket', views.delete_ticket, name='delete-ticket'),
]
