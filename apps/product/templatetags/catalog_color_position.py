from django import template
register = template.Library()

@register.filter(name='catalog_color_position')
def catalog_color_position(d, colors):
    item_width = 18
    return -((item_width + 7) *len(colors) / 2)