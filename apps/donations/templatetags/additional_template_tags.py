from django import template

register = template.Library()


@register.filter(name='queryset_ids_as_string')
def queryset_ids_as_string(somequery):
    result = ''
    for category in somequery:
        result += str(category.id)
    return result


@register.filter(name='queryset_ids_as_list')
def queryset_ids_as_list(somequery):
    result = []
    for category in somequery:
        result.append(category.id)
    return result


@register.filter(name="type_equal_to")
def type_filter(some_query, value):
    result = []
    for item in some_query:
        result.append(item) if item.type == value else False
    return result
