from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.shortcuts import render

from .models import Product, Company, Category, Season, ProductComposition, SizeScale
from django.db.models import Q
from django.contrib.auth.decorators import login_required, permission_required
from basket.models import Basket
from django.contrib.auth.models import Group, User
from django.db.models import Sum
from django.views.generic import ListView

# 1 Вариант
# def get_products(request: HttpRequest) -> HttpResponse:
#     products = Product.objects.filter(is_deleted=False)
#     return render(request, 'products/all_products.html', {'products': products})


# 2 Вариант - с учетом бокового меню "Filter"
# def get_products(request: HttpRequest) -> HttpResponse:
#     products = Product.objects.filter(is_deleted=False)
#     category_list = Category.objects.all()                    # Если запрос GET, то:
#     season_list = Season.objects.all()                        # функция извлекает ВСЕ данные товара с ForeignKey из БД
#     composition_list = ProductComposition.objects.all()
#     size_scale_list = SizeScale.objects.all()
#     company_list = Company.objects.all()
#
#     data = {
#         'products': products,
#         'categories': category_list,      # таким образом передали в шаблон 5 словарей:
#         'seasons': season_list,           # ДЛЯ УДОБСТВА заполнения этих полей в шаблоне - делаем их в виде
#         'compositions': composition_list, # выпадающего списка - см. models.py !!!
#         'size_scales': size_scale_list,
#         'companies': company_list,
#     }
#     return render(request, 'products/all_products.html', data)


# 3 Вариант - с учетом бокового меню "Filter" + Сумма количества товаров в иконке "Корзина"
# def get_products(request: HttpRequest) -> HttpResponse:
#     products = Product.objects.filter(is_deleted=False)
#     category_list = Category.objects.all()                    # Если запрос GET, то:
#     season_list = Season.objects.all()                        # функция извлекает ВСЕ данные товара с ForeignKey из БД
#     composition_list = ProductComposition.objects.all()
#     size_scale_list = SizeScale.objects.all()
#     company_list = Company.objects.all()
#
#     if request.user.is_authenticated:
#         basket_items = Basket.objects.filter(user=request.user)
#         total_quantity = basket_items.aggregate(Sum('quantity'))
#         total_price = sum(item.product.price * item.quantity for item in basket_items)
#
#         data = {
#             'products': products,
#             'categories': category_list,      # таким образом передали в шаблон 5 словарей:
#             'seasons': season_list,           # ДЛЯ УДОБСТВА заполнения этих полей в шаблоне - делаем их в виде
#             'compositions': composition_list, # выпадающего списка - см. models.py !!!
#             'size_scales': size_scale_list,
#             'companies': company_list,
#             'total_quantity': total_quantity.get('quantity__sum'),
#             'total_price': total_price
#         }
#
#     else:       # при выходе из своего аккаунта - мы НЕ должны передавать в шаблон кол-во товаров в корзине и сумму !
#         data = {
#             'products': products,
#             'categories': category_list,
#             'seasons': season_list,
#             'compositions': composition_list,
#             'size_scales': size_scale_list,
#             'companies': company_list,
#         }
#
#     return render(request, 'products/all_products.html', data)


# ПОЯСНЕНИЕ по использованию класса (ListView):

# Во фреймворке Django помимо функций можно использовать и КЛАССЫ ПРЕДСТАВЛЕНИЙ (контроллеры классов):
#
# CBV – Class-Based Views
#
# Классы представлений создаются на основе базовых классов фреймворка Django
# Чаще всего именно их применяют на практике, так как объектно-ориентированный подход, зачастую,
# позволяет заметно упростить код, сделать его более понятным и читабельным.

#
# - Класс ProductListView наследуется от ListView, который является ВСТРОЕННЫМ классом представлений в Django.
# Он используется для отображения списка объектов.
#
# - В нашем классе ProductListView, который наследуется от ListView, родительским классом является ListView.
# Когда вы вызываете super().get_context_data(**kwargs), вы вызываете метод get_context_data из класса ListView.
#
# - Класс ListView является частью Django и используется для отображения списков объектов.
# Он предоставляет множество встроенных функций, таких как "ПАГИНАЦИЯ" и "СОРТИРОВКА",
# которые можно использовать и переопределять в вашем классе представлений.
#
# - Функция get_context_data используется в Django, чтобы добавить дополнительные данные в контекст шаблона.
# Она часто переопределяется в классах представлений (views) для добавления или изменения данных,
# которые передаются в шаблон.
#
# Вот что делает эта функция:
#
# def get_context_data(self, *, object_list=None, **kwargs): - Это определение функции.
# Она принимает аргументы object_list и **kwargs. object_list по умолчанию равен None,
# а **kwargs позволяет передавать дополнительные именованные аргументы.
#
# context = super().get_context_data(**kwargs): - Здесь вызывается метод get_context_data родительского класса
# с помощью super(), и результат сохраняется в переменную context.
# Это позволяет СНАЧАЛА получить "стандартный контекст", который формируется родительским классом ListView.
#
# return context: Возвращает измененный контекст.

# Реализация get_context_data () по умолчанию в ListView добавляет возвращаемое значение get_queryset ()
# (которое просто возвращает self.набор запросов по умолчанию) в контекст как переменную objects_list.
#
# - Таким образом, эта функция позволяет вам добавить или изменить данные в контексте,
# который будет передан в шаблон. Например, вы можете добавить дополнительные переменные в контекст,
# которые будут доступны в вашем шаблоне.

# <!-- Pagination -->
class ProductListView(ListView):
    '''
    Определим свой собственный класс представления на базе класса ListView.
    Внутри определим атрибут model, который будет ссылаться на модель данных Product,
    связанной с этим списком. Фактически, строчка model = Product выберет все записи из таблицы Product
    и попытается отобразить их в виде списка, используя шаблон 'products/all_products.html'

    По умолчанию, данные из модели Product, указанной в классе представлений, помещаются в коллекцию object_list !!!
    Если в шаблоне вместо object_list мы хотим использовать другое обозначение (имя), то в классе HomeView???
    следует прописать атрибут context_object_name с указанием другого имени переменной:
    '''
    model = Product
    template_name = 'products/all_products.html'
    context_object_name = 'products' # а) по умолчанию object_list
                                     # б) {% for product in products %} --> 'products'
    paginate_by = 12

# 2 Вариант с учетом количества товаров и суммы товаров в корзине!
    def get_context_data(self, *, object_list=None, **kwargs):
        '''
        C помощью метода get_context_data() можно передавать любую информацию в шаблон !
        Интегрированная среда предлагает "полный формат записи" этого метода со всеми параметрами:

        def get_context_data(self, *, object_list=None, **kwargs):

        Я его так и оставлю, хотя, отсюда можно убрать то, что не используется.
        Далее, внутри метода мы первым делом должны повторить работу этого метода БАЗОВОГО класса ListView,
        используя строчку:
        '''
        context = super().get_context_data(**kwargs)
        '''
        Здесь super() – это обращение к БАЗОВОМУ классу и, далее, через точку, идет вызов аналогичного метода 
        с передачей ему возможных именованных параметров из словаря kwargs. 
        Сформированный БАЗОВЫЙ контекст мы сохраняем через переменную context, которая ссылается на словарь.
        В этой же функции мы можем добавить ДОПОЛНИТЕЛЬНЫЕ переменные в context, которые будут доступны в шаблоне.
        В конце метод get_context_data должен вернуть сформированный context.
        
        Реализация get_context_data() по умолчанию в ListView добавляет возвращаемое значение get_queryset()
        (которое просто возвращает self.набор запросов по умолчанию) в context как переменную objects_list.
        '''
        # Для того чтобы На ГЛАВНОЙ СТРАНИЦЕ показывать КОЛИЧЕСТВО ТОВАРОВ и СУММУ ТОВАРОВ в корзине!
        if self.request.user.is_authenticated:
            basket_items = Basket.objects.filter(user=self.request.user)
            total_quantity = basket_items.aggregate(Sum('quantity'))
            total_price = sum(item.product.price * item.quantity for item in basket_items)

            context['basket_items'] = basket_items
            context['total_quantity'] = total_quantity.get('quantity__sum')
            context['total_price'] = total_price

            context['categories'] = Category.objects.all()
            context['seasons'] = Season.objects.all()
            context['compositions'] = ProductComposition.objects.all()
            context['size_scales'] = SizeScale.objects.all()
            context['companies'] = Company.objects.all()
        # return context

        else:
            context['categories'] = Category.objects.all()
            context['seasons'] = Season.objects.all()
            context['compositions'] = ProductComposition.objects.all()
            context['size_scales'] = SizeScale.objects.all()
            context['companies'] = Company.objects.all()
        return context

    def get_queryset(self):
        '''
        Реализация get_context_data() по умолчанию в ListView добавляет возвращаемое значение get_queryset()
        (которое просто возвращает self.набор запросов по умолчанию) в context как переменную objects_list.

        Последний штрих, который мы сделаем в классе представления ProductListView – это добавим фильтрацию
        продуктов по полю is_deleted=False. Для этого существует специальный МЕТОД get_queryset,
        переопределяя который, можно указать как именно выбирать записи из модели Product.
        '''
        return Product.objects.filter(is_deleted=False)


def get_products_list(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        user = request.user
        products = Product.objects.filter(company__name_company=user)

        return render(request, 'products/products_list.html', {'products': products})
    else:
        return render(request, 'userAdmin/login.html')


# def get_products_category(request, category_id):
#     category_list = Category.objects.all()
#     products = Product.objects.filter(category__id=category_id).filter(is_deleted=False)
#     data = {
#         'products': products,
#         'categories': category_list,
#     }
#     return render(request, 'products/all_products.html', data)
    # return render(request, 'products/all_products.html', {'products': products})


# Фильтрация продуктов "по категориям" с учетом пагинации !
class ProductCategoryListView(ListView):
    model = Product
    template_name = 'products/all_products.html'
    context_object_name = 'products'
    paginate_by = 8

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['seasons'] = Season.objects.all()
        context['compositions'] = ProductComposition.objects.all()
        context['size_scales'] = SizeScale.objects.all()
        context['companies'] = Company.objects.all()
        return context

    def get_queryset(self):
        '''
        Здесь первым параметром указано имя category__id – это способ обращения к id таблицы Category
        через объект id модели Product. Далее, указываем,
        что поле id у категории должно быть равно параметру 'category_id' - т.е. self.kwargs['category_id'],
        который мы берем из словаря kwargs объекта класса ProductCategoryListView.
        Ключ category_id автоматически формируется по шаблону маршрута urls.py),
        в котором мы должны вместо функции указать класс представления:
        path('get-products-category/<int:category_id>/', ProductCategoryListView.as_view(), name='get-products-category')
        '''
        return Product.objects.filter(category__id=self.kwargs['category_id']).filter(is_deleted=False)


# def get_clothing(request):
#     products = Product.objects.filter(category__name_category='Сloth').filter(is_deleted=False)
#     return render(request, 'products/all_products.html', {'products': products})
#
#
# def get_shoes(request):
#     products = Product.objects.filter(category__name_category='Shoes').filter(is_deleted=False)
#     return render(request, 'products/all_products.html', {'products': products})
#
#
# def get_accessories(request):
#     products = Product.objects.filter(category__name_category='Accessories').filter(is_deleted=False)
#     return render(request, 'products/all_products.html', {'products': products})


# def get_by_name_product(request, name_prod):
#     products = Product.objects.filter(name_prod=name_prod).filter(is_deleted=False)
#
#     return render(request, 'products/all_products.html', {'products': products})


def get_pants(request):
    products = Product.objects.filter(name_prod='Pants').filter(is_deleted=False)
    return render(request, 'products/all_products.html', {'products': products})


def get_jumpers(request):
    products = Product.objects.filter(name_prod='Jumper').filter(is_deleted=False)
    return render(request, 'products/all_products.html', {'products': products})


def get_jeans(request):
    products = Product.objects.filter(name_prod='Jeans').filter(is_deleted=False)
    return render(request, 'products/all_products.html', {'products': products})


def get_jackets(request):
    products = Product.objects.filter(name_prod='Jacket').filter(is_deleted=False)
    return render(request, 'products/all_products.html', {'products': products})


def get_coats(request):
    products = Product.objects.filter(name_prod='Coat').filter(is_deleted=False)
    return render(request, 'products/all_products.html', {'products': products})


def get_shirts(request):
    products = Product.objects.filter(name_prod='Shirt').filter(is_deleted=False)
    return render(request, 'products/all_products.html', {'products': products})


def get_tshirts(request):
    products = Product.objects.filter(name_prod='T-shirt').filter(is_deleted=False)
    return render(request, 'products/all_products.html', {'products': products})


def get_boots(request):
    products = Product.objects.filter(name_prod='Boots').filter(is_deleted=False)
    return render(request, 'products/all_products.html', {'products': products})


def get_sneakers(request):
    products = Product.objects.filter(name_prod='Sneakers').filter(is_deleted=False)
    return render(request, 'products/all_products.html', {'products': products})


def get_moccasins(request):
    products = Product.objects.filter(name_prod='Moccasins').filter(is_deleted=False)
    return render(request, 'products/all_products.html', {'products': products})


def get_list_shoes(request):
    products = Product.objects.filter(name_prod='Shoes').filter(is_deleted=False)
    return render(request, 'products/all_products.html', {'products': products})


def get_ties(request):
    products = Product.objects.filter(name_prod='Tie').filter(is_deleted=False)
    return render(request, 'products/all_products.html', {'products': products})


def get_wallets(request):
    products = Product.objects.filter(name_prod='Wallet').filter(is_deleted=False)
    return render(request, 'products/all_products.html', {'products': products})


def get_belts(request):
    products = Product.objects.filter(name_prod='Belt').filter(is_deleted=False)
    return render(request, 'products/all_products.html', {'products': products})


def get_bags(request):
    products = Product.objects.filter(name_prod='Bag').filter(is_deleted=False)
    return render(request, 'products/all_products.html', {'products': products})


def get_scavers(request):
    products = Product.objects.filter(name_prod='Scarf').filter(is_deleted=False)
    return render(request, 'products/all_products.html', {'products': products})


# 1 Вариант
# def product_details(request, product_id):
#     size_scale_list = SizeScale.objects.all()
#     product = Product.objects.get(id=product_id)
#     data = {
#         'size_scales': size_scale_list,
#         'product': product
#     }
#     return render(request, 'products/product_details.html', data)


# Основной вариант !
# 2 Вариант - с учетом Cуммы количества товаров в иконке "Корзина"
def product_details(request, product_id):
    product = Product.objects.get(id=product_id)
    """ Выводим только те размеры, которые есть у данного АРТИКУЛА. """
    sizes_product_list = SizeScale.objects.filter(product__article=product.article)
    print(sizes_product_list)
    # size_scale_list = SizeScale.objects.all()[5:]

    if request.user.is_authenticated:
        basket_items = Basket.objects.filter(user=request.user)
        total_quantity = basket_items.aggregate(Sum('quantity'))
        total_price = sum(item.product.price * item.quantity for item in basket_items)

        data = {
            'sizes_product_list': sizes_product_list,
            'product': product,
            'total_quantity': total_quantity.get('quantity__sum'),
            'total_price': total_price,
            'basket_items': basket_items,
        }

    else:          # Если мы НЕ авторизованы !!! - мы НЕ должны передавать в шаблон количество товаров в корзине и цены!
        data = {
            'product': product,
            'sizes_product_list': sizes_product_list,
        }
    return render(request, 'products/product_details.html', data)


# 2.1 Вариант с выбором размера товара при входе в "DETAILS"
def select_size(request, product_id):
    current_page = request.META.get('HTTP_REFERER')
    product = Product.objects.get(id=product_id)

    if request.method == 'POST':
        size_select_id = request.POST.get('size_product_id')  # Получим ID выбранного размера
        # size = SizeScale.objects.get(id=size_select_id)
        product.size_scale.size_scale = size_select_id
        product.save()
        print(size_select_id)

        # if request.POST.get('size_prod') == '':
        #     product.size = None

    return HttpResponseRedirect(current_page)


def get_product_by_id(request, product_id):
    product = Product.objects.get(id=product_id)
    category_list = Category.objects.all()
    season_list = Season.objects.all()
    composition_list = ProductComposition.objects.all()
    size_scale_list = SizeScale.objects.all()
    company_list = Company.objects.all()

    data = {
        'product': product,
        'categories': category_list,
        'seasons': season_list,
        'compositions': composition_list,
        'size_scales': size_scale_list,
        'companies': company_list,
    }

    return render(request, 'products/get_product_by_id.html', data)


# @login_required  # декоратор, требующий аутентификации пользователя
@permission_required('products.add1')  # декоратор, требующий наличия определенных разрешений
def add_product(request):
    """
    Представление для добавления нового автомобиля в автопарк.
    Обрабатывает как GET, так и POST запросы.
    Для GET запросов извлекает список марок и типов автомобилей и рендерит шаблон 'add_product.html' с данными.
    Для POST запросов извлекает детали автомобиля из запроса и сохраняет новый автомобиль
    в базу данных, затем перенаправляется на URL 'get-products'.
    """
    if request.method == 'GET':
        category_list = Category.objects.all()              # Если запрос GET, то:
        season_list = Season.objects.all()                  # функция извлекает все данные товара с ForeignKey из БД
        composition_list = ProductComposition.objects.all()
        size_scale_list = SizeScale.objects.all()
        company_list = Company.objects.all()

        data = {                                   # таким образом передали в шаблон 5 словарей:
            'categories': category_list,           # ДЛЯ УДОБСТВА заполнения этих полей в шаблоне - делаем их в виде
            'seasons': season_list,                # выпадающего списка - см. models.py !!!
            'compositions': composition_list,
            'size_scales': size_scale_list,
            'companies': company_list,
        }
        return render(request, 'products/add_product.html', data)

        # функция render() возвращает шаблон 'add_product.html', где мы заполняем ВСЕ данные для НОВОГО товара
        # см.models.py !!!

    # Если метод запроса равен 'POST', то функция извлекает данные из запроса POST из заполненных полей шаблона
    if request.method == 'POST':
        name_prod = request.POST.get('name_prod')
        article = request.POST.get('article')
        description = request.POST.get('description')
        color = request.POST.get('color')
        price = request.POST.get('price')
        product_count = request.POST.get('product_count')
        category_id = request.POST.get('category_id')
        season_id = request.POST.get('season_id')
        product_composition_id = request.POST.get('product_composition_id')
        size_scale_id = request.POST.get('size_scale_id')
        company_id = request.POST.get('company_id')
        image = request.FILES.get('image')

        try:
            if (not name_prod or not article or not description or not color or not price or not product_count
                    or not category_id or not season_id or not product_composition_id or not size_scale_id
                    or not company_id or not image):
                raise ValidationError('All fields are required')

            name_prod = str(name_prod)
            if not name_prod.isalpha():  # возвращает True, если все символы в строке являются буквами!
                raise ValidationError('Field Name product must contain only letters')

            article = str(article)
            if not isinstance(article, str):
                raise ValidationError('Field must be a string')

            description = str(description)
            if not isinstance(description, str):
                raise ValidationError('Field must be a string')

            color = str(color)
            if not color.isalpha():
                raise ValidationError('Field color must contain only letters')

            price = float(price)
            if price <= 0:
                raise ValidationError('Price must be greater than 0')

            if not isinstance(price, float):
                raise ValidationError('Field must be a number')

            product_count = int(product_count)
            if product_count <= 0:
                raise ValidationError('Count must be greater than 0')

            if not isinstance(product_count, int):
                raise ValidationError('Field must be a number')

            category = Category.objects.get(id=category_id)  # Находим КАТЕГОРИЮ по соотв-щему идентификатору
            season = Season.objects.get(id=season_id)          # Находим CЕЗОН по соотв-щему ID
            product_composition = ProductComposition.objects.get(id=product_composition_id)  # СОСТАВ
            size_scale = SizeScale.objects.get(id=size_scale_id)  # РАЗМЕР
            company = Company.objects.get(id=company_id)  # Производителя

            product = Product.objects.create(               # Создаем НОВЫЙ объект Product и сохраняем его в БД
                name_prod=name_prod,
                article=article,
                description=description,
                color=color,
                price=price,
                product_count=product_count,
                category=category,
                season=season,
                product_composition=product_composition,
                size_scale=size_scale,
                company=company,
                image=image,
            )
            product.save()

            return HttpResponseRedirect(reverse('get-products-list'))
            # return HttpResponseRedirect(reverse('get-products'))

        except ValidationError as e:
            error = str(e)

            category_list = Category.objects.all()          # Т.е. если ошибка, то должны вернуться к шаблону из GET:
            season_list = Season.objects.all()              # см. начало метода !!!
            composition_list = ProductComposition.objects.all()
            size_scale_list = SizeScale.objects.all()
            company_list = Company.objects.all()

            data = {
                'categories': category_list,
                'seasons': season_list,
                'compositions': composition_list,
                'size_scales': size_scale_list,
                'companies': company_list,
                'error': error,
            }
            return render(request, 'products/add_product.html', data)


def update_product(request, product_id: int):
    if request.method == 'POST':
        product_name_prod = request.POST.get('name_prod')
        product_article = request.POST.get('article')
        product_description = request.POST.get('description')
        product_color = request.POST.get('color')
        product_price = request.POST.get('price')
        product_product_count = request.POST.get('product_count')
        category_id = request.POST.get('category_id')
        season_id = request.POST.get('season_id')
        product_composition_id = request.POST.get('product_composition_id')
        size_scale_id = request.POST.get('size_scale_id')
        company_id = request.POST.get('company_id')
        product_image = request.FILES.get('image')

        try:
            product = Product.objects.get(id=product_id)

            if (not product_name_prod or not product_article or not product_description or not product_color
                    or not product_price or not product_product_count):

                raise ValidationError('All fields are required')

            product_price = float(product_price)
            if product_price <= 0:
                raise ValidationError('Price must be greater than 0')

            if not isinstance(product_price, float):
                raise ValidationError('Field must be a number')

            product_product_count = int(product_product_count)
            if product_product_count <= 0:
                raise ValidationError('Count must be greater than 0')

            if not isinstance(product_product_count, int):
                raise ValidationError('Field must be a number')

            product.category = Category.objects.get(id=category_id)
            product.season = Season.objects.get(id=season_id)
            product.product_composition = ProductComposition.objects.get(id=product_composition_id)
            product.size_scale = SizeScale.objects.get(id=size_scale_id)
            product.company = Company.objects.get(id=company_id)
            product.name_prod = product_name_prod
            product.article = product_article
            product.description = product_description
            product.color = product_color
            product.price = product_price
            product.product_count = product_product_count
            if product_image:
                product.image = product_image

            product.save()

            return HttpResponseRedirect(reverse('get-products-list'))
            # return HttpResponseRedirect(reverse('get-product-by-id', args=[product_id]))

        except ValidationError as e:
            error = str(e)

            product = Product.objects.get(id=product_id)
            category_list = Category.objects.all()
            season_list = Season.objects.all()
            composition_list = ProductComposition.objects.all()
            size_scale_list = SizeScale.objects.all()
            company_list = Company.objects.all()

            data = {
                'product': product,
                'categories': category_list,
                'seasons': season_list,
                'compositions': composition_list,
                'size_scales': size_scale_list,
                'companies': company_list,
                'error': error,
            }
            return render(request, 'products/update_product.html', data)

    else:
        product = Product.objects.get(id=product_id)
        category_list = Category.objects.all()
        season_list = Season.objects.all()
        composition_list = ProductComposition.objects.all()
        size_scale_list = SizeScale.objects.all()
        company_list = Company.objects.all()

        data = {
            'product': product,
            'categories': category_list,
            'seasons': season_list,
            'compositions': composition_list,
            'size_scales': size_scale_list,
            'companies': company_list,
        }

        return render(request, 'products/update_product.html', data)


# @permission_required('products.change2')
# def update_product(request: HttpRequest, product_id: int):
#     """
#     Обновляет объект товара с предоставленной информацией из HttpRequest.
#
#     Параметры:
#         request (HttpRequest): Объект HTTP-запроса.
#         product_id (int): Идентификатор обновляемого товара.
#
#     Возвращает:
#         HttpResponseRedirect: Перенаправляет на URL 'get-products' после обновления товара.
#     """
#     if request.method != 'POST':
#         return HttpResponse('Invalid request method')
#
#     product = Product.objects.get(id=product_id)       # Получаем объект товара по ID
#
#                                                        # Получаем "НОВЫЕ" ДАННЫЕ:
#     product_name_prod = request.POST.get('name_prod')
#     product_article = request.POST.get('article')
#     product_description = request.POST.get('description')
#     product_color = request.POST.get('color')
#     product_price = request.POST.get('price')
#     product_product_count = request.POST.get('product_count')
#     category_id = request.POST.get('category_id')
#     season_id = request.POST.get('season_id')
#     product_composition_id = request.POST.get('product_composition_id')
#     size_scale_id = request.POST.get('size_scale_id')
#     company_id = request.POST.get('company_id')
#     image = request.FILES.get('image')
#                                         # Идентификаторы 'КАТЕГОРИИ', 'СЕЗОНА' и т.д. из POST-запроса!!!
#                                         # Почему назвали category_id и season_id - из Models.py -> Class Product !!!
#                                         # category = models.ForeignKey(Category...)
#                                         # season = models.ForeignKey(Season ...)
#
#     category = Category.objects.get(id=category_id)           # Находим КАТЕГОРИЮ по соотв-щим идентификатору
#     season = Season.objects.get(id=season_id)
#     product_composition = ProductComposition.objects.get(id=product_composition_id)
#     size_scale = SizeScale.objects.get(id=size_scale_id)
#     company = Company.objects.get(id=company_id)
#
#                                               # ОБНОВЛЯЕМ данные товара по заданным полям!
#     product.name_prod = product_name_prod
#     product.article = product_article
#     product.description = product_description
#     product.color = product_color
#     product.price = product_price
#     product.product_count = product_product_count
#     product.category = category
#     product.season = season
#     product.product_composition = product_composition
#     product.size_scale = size_scale
#     product.company = company
#     product.image = image
#
#     product.save()
#
#     return HttpResponseRedirect(reverse('get-products-list'))


def delete_product(request, product_id: int):
    if request.method == 'POST':
        product = Product.objects.get(id=product_id)

        product.is_deleted = True
        product.save()
        return HttpResponseRedirect(reverse('get-products-list'))
    else:
        product = Product.objects.get(id=product_id)
        data = {
            'product_id': product.id,
            'name_prod': product.name_prod,
            'article': product.article,
        }
        return render(request, 'products/delete_product.html', data)


def search_product(request):
    if request.method == 'GET':
        return render(request, 'products/all_products.html')
    else:
        search_string = request.POST.get('search_string')
        try:
            product_list = Product.objects.filter(is_deleted=False).filter(
                Q(name_prod__icontains=search_string)
                | Q(article__icontains=search_string)
                | Q(color__icontains=search_string)
                # | Q(price__icontains=search_string)
                | Q(category__name_category__icontains=search_string)
                | Q(season__name_season__icontains=search_string)
                | Q(product_composition__product_composition__icontains=search_string)
                # | Q(size_scale__size_scale__icontains=search_string)
                | Q(company__name_company__icontains=search_string)
            )
            if not product_list:
                # product_list = Product.objects.all()
                return render(request, 'products/nothing_is_find.html')

        except ValidationError:
            product_list = Product.objects.filter(is_deleted=False)

        return render(request, 'products/all_products.html', {'products': product_list})

# P.S: как ставить:
# Q(category__name_category__icontains=search_string)
# category - берем из: class Product(models.Model)
# name_category берем из: class Category(models.Model)

# Просто примеры:
# books = Book.objects.filter(Q(author='John Smith') & Q(year=2021) & Q(genre='Fiction'))
# books = Book.objects.filter(author='John Smith').filter(year=2021)


# БОКОВОЙ ФИЛЬТР (без учета пагинации)

def search_products_list(request):
    category_list = Category.objects.all()
    season_list = Season.objects.all()
    composition_list = ProductComposition.objects.all()
    size_scale_list = SizeScale.objects.all()
    company_list = Company.objects.all()

        # Если метод запроса 'POST', то функция извлекает данные из заполненных полей шаблона!
    if request.method == 'POST':
        category_id = request.POST.get('category_id')     # это name="category_id" из шаблона all_products.html
        season_id = request.POST.get('season_id')         # это name="season_id"
        product_composition_id = request.POST.get('product_composition_id')
        size_scale_id = request.POST.get('size_scale_id')
        company_id = request.POST.get('company_id')

        products_list = Product.objects.all().filter(is_deleted=False)

        if category_id:
            category = Category.objects.get(id=category_id)       # Находим КАТЕГОРИЮ по соотв-щему идентификатору
            products_list = products_list.filter(category=category)

        if season_id:
            season = Season.objects.get(id=season_id)            # Находим КАТЕГОРИЮ по соотв-щему идентификатору
            products_list = products_list.filter(season=season)

        if product_composition_id:
            product_composition = ProductComposition.objects.get(id=product_composition_id)
            products_list = products_list.filter(product_composition=product_composition)

        if size_scale_id:
            size_scale = SizeScale.objects.get(id=size_scale_id)
            products_list = products_list.filter(size_scale=size_scale)

        if company_id:
            company = Company.objects.get(id=company_id)
            products_list = products_list.filter(company=company)

        if not products_list:
            # products_list = Product.objects.all()
            return render(request, 'products/nothing_is_find.html')

        data = {
            'products': products_list,
            'categories': category_list,
            'seasons': season_list,
            'compositions': composition_list,
            'size_scales': size_scale_list,
            'companies': company_list,
        }
        return render(request, 'products/all_products.html', data)


# БОКОВОЙ ФИЛЬТР (с учетом пагинации)
# class ProductsFiltersListView(ListView):
#     model = Product
#     template_name = 'products/all_products.html'
#     context_object_name = 'products'
#     paginate_by = 8
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['categories'] = Category.objects.all()
#         context['seasons'] = Season.objects.all()
#         context['compositions'] = ProductComposition.objects.all()
#         context['size_scales'] = SizeScale.objects.all()
#         context['companies'] = Company.objects.all()

        # context['category_id'] = self.request.POST.get('category_id')
        # context['season_id'] = self.request.POST.get('season_id')
        # context['product_composition_id'] = self.request.POST.get('product_composition_id')
        # context['size_scale_id'] = self.request.POST.get('size_scale_id')
        # context['company_id'] = self.request.POST.get('company_id')

        # return context

    # def post(self, request, *args, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #
    #     context['category_id'] = self.request.POST.get('category_id')
    #     context['season_id'] = self.request.POST.get('season_id')
    #     context['product_composition_id'] = self.request.POST.get('product_composition_id')
    #     context['size_scale_id'] = self.request.POST.get('size_scale_id')
    #     context['company_id'] = self.request.POST.get('company_id')

        # if self.request.method == 'POST':
        #     self.kwargs['category_id'] = self.request.POST('category_id')
        #     self.kwargs['season_id'] = self.request.POST('season_id')
        #     self.kwargs['product_composition_id'] = self.request.POST('product_composition_id')
        #     self.kwargs['size_scale_id'] = self.request.POST('size_scale_id')
        #     self.kwargs['company_id'] = self.request.POST('company_id')

        # return context

    # def get_queryset(self):
    #     queryset = super().get_queryset()
        # queryset = queryset.filter(is_deleted=False)

        # if self.request.method == 'POST':
        #     category_id = self.request.POST.get('category_id')
        #     season_id = self.request.POST.get('season_id')
        #     product_composition_id = self.request.POST.get('product_composition_id')
        #     size_scale_id = self.request.POST.get('size_scale_id')
        #     company_id = self.request.POST.get('company_id')

        # if self.request.method == 'GET':
        # self.kwargs['category_id'] = self.request.GET.get('category_id')
        # self.kwargs['season_id'] = self.request.GET.get('season_id')
        # self.kwargs['product_composition_id'] = self.request.GET.get('product_composition_id')
        # self.kwargs['size_scale_id'] = self.request.GET.get('size_scale_id')
        # self.kwargs['company_id'] = self.request.GET.get('company_id')

        # if category_id == ['category_id']:
        # if category_id := self.kwargs['category_id']:
        #     queryset = queryset.filter(category__id=category_id).filter(is_deleted=False)
        # if season_id := self.kwargs['season_id']:
        #     queryset = queryset.filter(season__id=season_id).filter(is_deleted=False)
        # if product_composition_id := self.kwargs['product_composition_id']:
        #     queryset = queryset.filter(product_composition__id=product_composition_id).filter(is_deleted=False)
        # if size_scale_id := self.kwargs['size_scale_id']:
        #     queryset = queryset.filter(size_scale__id=size_scale_id).filter(is_deleted=False)
        # if company_id := self.kwargs['company_id']:
        #     queryset = queryset.filter(company__id=company_id).filter(is_deleted=False)
        #
        # return queryset


# ПРОСТО ПРОБОВАЛ!!!
    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['products'] = Product.objects.all()
    #     context['categories'] = Category.objects.all()
    #     context['seasons'] = Season.objects.all()
    #     context['compositions'] = ProductComposition.objects.all()
    #     context['size_scales'] = SizeScale.objects.all()
    #     context['companies'] = Company.objects.all()
    #
    #     return context
    #
    # def post(self, request, *args, **kwargs):
    #     if self.request.method == 'POST':
    #         self.kwargs['category_id'] = self.request.POST.get('category_id')
    #         self.kwargs['season_id'] = self.request.POST.get('season_id')
    #         self.kwargs['product_composition_id'] = self.request.POST.get('product_composition_id')
    #         self.kwargs['size_scale_id'] = self.request.POST.get('size_scale_id')
    #         self.kwargs['company_id'] = self.request.POST.get('company_id')
    #
    #     # return self.get(self.request, **kwargs)
    #
    #         return self.get(self.request, **kwargs)
    #
    # def get_queryset(self):
    #
    #     products_list = Product.objects.all().filter(is_deleted=False)
    #
    #     if self.kwargs['category_id']:
    #         category = Category.objects.get(id=self.kwargs['category_id'])
    #         products_list = products_list.filter(category=category)
    #     # if 'season_id' in self.kwargs:
    #     if self.kwargs['season_id']:
    #         season = Season.objects.get(id=self.kwargs['season_id'])
    #         products_list = products_list.filter(season=season)
    #     if self.kwargs['product_composition_id']:
    #         product_composition = ProductComposition.objects.get(id=self.kwargs['product_composition_id'])
    #         products_list = products_list.filter(product_composition=product_composition)
    #     if self.kwargs['size_scale_id']:
    #         size_scale = SizeScale.objects.get(id=self.kwargs['size_scale_id'])
    #         products_list = products_list.filter(size_scale=size_scale)
    #     if self.kwargs['company_id']:
    #         company = Company.objects.get(id=self.kwargs['company_id'])
    #         products_list = products_list.filter(company=company)
    #
    #     return products_list






        # return Product.objects.filter(category__id=self.kwargs['category_id']).filter(is_deleted=False)

        # category = Category.objects.get(id=self.kwargs['category_id'])
        # products_list = products_list.filter(category=category)

#
#         context['products'] = Product.objects.all().filter(is_deleted=False)
#
#         # if request.method == 'POST':
#         #     category_id = request.POST.get('category_id')
#         #     season_id = request.POST.get('season_id')
#         #     product_composition_id = request.POST.get('product_composition_id')
#         #     size_scale_id = request.POST.get('size_scale_id')
#         #     company_id = request.POST.get('company_id')
#         #
#         #     context['category_id'] = Category.objects.get(category__id=category_id)
#         #     context['season_id'] = Category.objects.get(season__id=season_id)
#         #     context['product_composition_id'] = Category.objects.get(product_composition__id=product_composition_id)
#         #     context['size_scale_id'] = Category.objects.get(size_scale__id=size_scale_id)
#         #     context['company_id'] = Category.objects.get(company__id=company_id)
#
#     #     context['category_id'] = Category.objects.get(category__id=category_id)
#     #     context['seasons'] = Season.objects.all()
#     #     context['compositions'] = ProductComposition.objects.all()
#     #     context['size_scales'] = SizeScale.objects.all()
#     #     context['companies'] = Company.objects.all()
#         return context
#
#
#         return (Product.objects.
#                 filter(category__id=self.kwargs['category_id']).
#                 filter(season__id=self.kwargs['season_id']).
#                 filter(product_composition__id=self.kwargs['product_composition_id']).
#                 filter(size_scale__id=self.kwargs['size_scale_id']).
#                 filter(company__id=self.kwargs['company_id']).
#                 filter(is_deleted=False))



# class ProductCategoryListView(ListView):
#     model = Product
#     template_name = 'products/all_products.html'
#     context_object_name = 'products'
#     paginate_by = 8
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['categories'] = Category.objects.all()
#         context['seasons'] = Season.objects.all()
#         context['compositions'] = ProductComposition.objects.all()
#         context['size_scales'] = SizeScale.objects.all()
#         context['companies'] = Company.objects.all()
#         return context
#
#     def get_queryset(self):
#         return Product.objects.filter(category__id=self.kwargs['category_id']).filter(is_deleted=False)


# Убрать ДУБЛИКАТЫ ИЗ СЛОВАРЯ в python:

# Способ 1: Использование словаря с уникальными значениями
# original_dict = {'a': 1, 'b': 2, 'c': 1, 'd': 3}
# unique_dict = {}
# for key, value in original_dict.items():
#     if value not in unique_dict.values():
#         unique_dict[key] = value
#
# print(unique_dict)
# Вывод: {'a': 1, 'b': 2, 'd': 3}


# Способ 2: Использование словаря с уникальными ключами
#
# original_dict = {'a': 1, 'b': 2, 'c': 1, 'd': 3}
# unique_dict = dict.fromkeys(original_dict.keys())
#
# print(unique_dict)
# Вывод: {'a': None, 'b': None, 'c': None, 'd': None}


# Способ 3: Использование словаря с уникальными парами ключ-значение !
# Если вам нужно сохранить уникальные пары ключ-значение, можно использовать set для проверки уникальности:
# original_dict = {'a': 1, 'b': 2, 'c': 1, 'd': 3}
# unique_dict = {}
# seen_values = set()
# for key, value in original_dict.items():
#     if value not in seen_values:
#         unique_dict[key] = value
#         seen_values.add(value)
#
# print(unique_dict)
# Вывод: {'a': 1, 'b': 2, 'd': 3}