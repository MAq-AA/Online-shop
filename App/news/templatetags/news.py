from django import template
from shop.models import *


register = template.Library()


@register.inclusion_tag('news/provider_list.html')
def get_providers():
    providers = Provider.object.all()
    return {'providers': providers}
