from django.contrib.auth.models import User
from django.db import models


class TicketStatus(models.Model):
    name = models.CharField(max_length=50)


class TicketCategory(models.Model):
    name = models.CharField(max_length=50)


class Ticket(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey(TicketStatus, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(TicketCategory, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
