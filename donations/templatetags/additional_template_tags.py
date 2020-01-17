from django import template

register = template.Library()


@register.filter(name='show_queryset_ids')
def show_cat_ids(somequery):
    result = ''
    for category in somequery:
        result += str(category.id)
    return result
