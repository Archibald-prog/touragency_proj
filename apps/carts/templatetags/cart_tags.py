from django import template

from apps.helpers import GetAdditionalData

register = template.Library()


@register.simple_tag()
def user_carts(request):
    return GetAdditionalData.get_user_cart(request)


@register.simple_tag()
def roomclass_options():
    return GetAdditionalData.get_roomclasses()
