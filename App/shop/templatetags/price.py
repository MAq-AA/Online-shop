from django import template
from ..models import *
from auth_user.models import Profile

register = template.Library()


@register.filter
def replacer(value):
    value = int(value)
    value = '{0:,}'.format(value).replace(',', ' ') + "&nbsp<b>₽</b>"
    return value


@register.simple_tag(takes_context=True)
def bought(context, prod_id):
    b = Basket.object.get(profile=Profile.object.get(user=context['user'])).products.filter(id=prod_id).count()
    if not b:
        button = f"<button name='add' class='add-to-basket-button' value='{prod_id}'>Добавить в корзину</button>"
    else:
        button = f"<button name='to-basket' class='go-to-basket-button' value='{prod_id}'>Перейти в корзину</button>"
    return button


@register.inclusion_tag('shop/provider_list.html')
def get_providers():
    providers = Provider.object.all()
    return {'provider': providers}
