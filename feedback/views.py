from django.shortcuts import HttpResponseRedirect
from .models import Ticket, TicketStatus, TicketCategory
from django.urls import reverse
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required

# Вариант 1 - через MODAL WINDOW
# def create_ticket(request):
#     title = request.POST.get('title')
#     description = request.POST.get('description')
#     category_id = request.POST.get('category_id')
#     user = request.user
#
#     ticket_status = TicketStatus.objects.get(id=1)
#     ticket_category = TicketCategory.objects.get(id=category_id)
#
#     ticket = Ticket.objects.create(
#         title=title,
#         description=description,
#         status=ticket_status,
#         category=ticket_category,
#         user=user,
#     )
#     ticket.save()
#
#     return HttpResponseRedirect(reverse('get-products'))


# Вариант 2 - через ШАБЛОН
@login_required(login_url='login')
def create_ticket(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category_id = request.POST.get('category_id')
        user = request.user

        try:
            if not title or not description or not category_id:
                raise ValidationError('All fields are required')

            ticket_status = TicketStatus.objects.get(id=1)
            ticket_category = TicketCategory.objects.get(id=category_id)

            ticket = Ticket.objects.create(
                title=title,
                description=description,
                status=ticket_status,
                category=ticket_category,
                user=user,
            )
            ticket.save()

            return HttpResponseRedirect(reverse('ticket-list'))

        except ValidationError as e:
            error = str(e)

            category_list = TicketCategory.objects.all()
            data = {
                'categories': category_list,
                'error': error,
            }
            return render(request, 'feedback/add_ticket.html', data)

    else:
        category_list = TicketCategory.objects.all()
        data = {
            'categories': category_list,
        }
        return render(request, 'feedback/add_ticket.html', data)


@login_required(login_url='login')
def ticket_list(request):
    user = request.user
    tickets = Ticket.objects.filter(user=user)
    return render(request, 'feedback/ticket_list.html', {'tickets': tickets})


def ticket_reviews(request):
    ticket_category = TicketCategory.objects.get(id=3)
    tickets = Ticket.objects.filter(category=ticket_category)
    return render(request, 'feedback/reviews_list.html', {'tickets': tickets})


def ticket_detail(request, ticket_id: int):
    ticket = Ticket.objects.get(id=ticket_id)
    return render(request, 'feedback/ticket_detail.html', {'ticket': ticket})


def delete_ticket(request, ticket_id: int):
    ticket = Ticket.objects.get(id=ticket_id)
    ticket.delete()
    return redirect('ticket-list')
