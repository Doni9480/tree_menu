from django import template

from menu.models import Menu, MenuItem

register = template.Library()


@register.inclusion_tag("template_tags/menu.html", takes_context=True)
def draw_menu(context, slug):
    try:
        # menu = Menu.objects.prefetch_related("menu_items__children").get(slug=slug)
        menu = MenuItem.objects.prefetch_related('children').filter(menu__slug=slug)
        return {"menu": menu, "context": context}
    except Menu.DoesNotExist:
        return {"menu": "", "context": context}


@register.inclusion_tag("template_tags/dropdown.html", takes_context=True)
def draw_dropdown(context, item):
    request_path = context.request.path
    return {"item": item, "request_path": request_path}


