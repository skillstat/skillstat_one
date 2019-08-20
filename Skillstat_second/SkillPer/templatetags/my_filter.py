from django import template

register = template.Library()
@register.filter(name='type_judge')
def type_judge(data):
    return isinstance(data, tuple)
