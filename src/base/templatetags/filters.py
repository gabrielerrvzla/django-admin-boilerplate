from django import template

register = template.Library()


@register.filter(name="has_active_child")
def has_active_child(item, current_url_name):
    children = item.get("children", [])

    for child in children:
        if child["url"] == current_url_name:
            return True

        if "active_children" in child and current_url_name in child["active_children"]:
            return True

    return False


@register.filter(name="get_attr")
def get_attr(value, arg):
    value = getattr(value, arg, "")

    if value is None:
        value = "-"

    if value is True:
        value = "Si"

    if value is False:
        value = "No"

    return value
