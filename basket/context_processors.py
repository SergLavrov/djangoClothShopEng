from basket.models import Basket


def basket_context(request):
    return {'basket': Basket(request)}
