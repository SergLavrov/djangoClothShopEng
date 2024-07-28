from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import Basket, Product, Payment, Delivery, Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db.models import Sum

"""
in_basket(запрос): В этом представлении отображается содержимое корзины покупок.
Он извлекает элементы корзины, связанные с текущим пользователем, 
вычисляет общее количество и цену товаров в корзине, а затем визуализирует шаблон 
для отображения элементов корзины вместе с общей ценой.

add_to_basket(request, product_id): Когда пользователь нажимает кнопку «Добавить в корзину» 
на товаре, этот просмотр срабатывает. Он добавляет выбранный товар в корзину пользователя. 
Если товар уже находится в корзине, количество увеличивается. Затем он перенаправляет 
пользователя в представление корзины, чтобы отобразить обновленное содержимое корзины.

delete_from_basket(request, item_id): Это представление обрабатывает удаление товара из корзины.
Он принимает идентификатор товара в качестве параметра, извлекает соответствующий товар корзины 
и удаляет его из базы данных. После удаления он перенаправляет пользователя в представление корзины, 
чтобы отразить обновленную корзину.
"""


@login_required(login_url='login')
def in_basket(request):
    basket_items = Basket.objects.filter(user=request.user)
    total_quantity = basket_items.aggregate(Sum('quantity'))
    # total_quantity = sum(item.quantity for item in basket_items)
    total_price = sum(item.product.price * item.quantity for item in basket_items)
    data = {
        'basket_items': basket_items,
        'total_quantity': total_quantity.get('quantity__sum'),
        # 'total_quantity': total_quantity,
        'total_price': total_price
    }
    return render(request, 'basket/basket.html', data)


@login_required(login_url='login')
def add_to_basket(request, product_id: int):
    try:
        product = Product.objects.get(id=product_id)
        product_count = Product.objects.get(id=product_id).product_count
        basket_item, created = Basket.objects.get_or_create(product=product, user=request.user)

        basket_item.quantity += 1
        basket_item.save()

        if basket_item.quantity > product_count:
            raise ValueError('Not enough products in stock')

    except ValueError as e:
        error = str(e)

        product = Product.objects.get(id=product_id)
        basket_item, created = Basket.objects.get_or_create(product=product, user=request.user)
        basket_item.quantity -= 1
        basket_item.save()
        return render(request, 'basket/no_product_in_stock.html', {'error': error})

    return redirect('in-basket')


def no_product_in_stock(request):
    return render(request, 'basket/no_product_in_stock.html')


@login_required
def delete_from_basket(request, item_id):
    basket_item = Basket.objects.get(id=item_id)
    basket_item.delete()
    return redirect('in-basket')


"""
Нам нужно использовать созданные модели заказов для сохранения товаров,
содержащихся в корзине для покупок, когда пользователь наконец пожелает разместить заказ.
Функции создания нового заказа будут работать следующим образом:

1.Мы предоставляем форму заказа для заполнения пользовательских данных.

2.Сохраняем данные введенные пользователем в форме в базу данных. Создается новый экземпляр заказа 
с данными, введенными пользователями, а затем создается связанный экземпляр OrderItem 
для каждого товара в корзине.

3.Очистищаем все содержимое корзины и перенаправляем пользователей на страницу success
"""


def create_order(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        city = request.POST.get('city')
        address = request.POST.get('address')
        postcode = request.POST.get('postcode')
        delivery_id = request.POST.get('delivery_id')
        payment_id = request.POST.get('payment_id')

        try:
            if ((not first_name) or (not last_name) or (not phone) or (not email) or (not city) or (not address)
                    or (not postcode)):
                raise ValidationError('All fields are required!')

            postcode = int(postcode)
            if len(str(postcode)) != 6:
                raise ValidationError('Incorrect postcode!')

            if not isinstance(postcode, int):
                raise ValidationError('Field must be a number')

            delivery = Delivery.objects.get(id=delivery_id)
            payment = Payment.objects.get(id=payment_id)

            order = Order.objects.create(
                user=request.user,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                email=email,
                city=city,
                address=address,
                postcode=postcode,
                delivery=delivery,
                payment=payment
            )
            order.save()

            basket = Basket.objects.filter(user=request.user)
            for item in basket:

                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity
                )
                item.delete()

            return render(request, 'basket/order_success.html', {'order': order})

        except ValidationError as e:
            error = str(e)

            delivery_list = Delivery.objects.all()
            payment_list = Payment.objects.all()

            data = {
                'delivery_list': delivery_list,
                'payment_list': payment_list,
                'error': error,
            }
            return render(request, 'basket/create_order.html', data)

    else:
        if request.method == 'GET':
            delivery_list = Delivery.objects.all()
            payment_list = Payment.objects.all()
            data = {
                'delivery_list': delivery_list,
                'payment_list': payment_list
            }
            return render(request, 'basket/create_order.html', data)


def order_list(request):
    orders = Order.objects.all()
    return render(request, 'basket/order_list.html', {'orders': orders})


def is_processed(request, order_id: int):
    if request.method == 'POST':
        order = Order.objects.get(id=order_id)
        order_is_processed = request.POST.get('is_processed')

        order.is_processed = order_is_processed == 'on'
        order.save()
        return HttpResponseRedirect(reverse('order-list'))


def delete_order(request, order_id: int):
    order = Order.objects.get(id=order_id)
    order.delete()
    return HttpResponseRedirect(reverse('order-list'))
