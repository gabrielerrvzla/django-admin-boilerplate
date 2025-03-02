from django.core.cache import cache
from django.utils.translation import gettext_lazy as _
from django.conf import settings


def filter_menu_by_permissions(menu_items, user):
    user_perms = user.get_all_permissions()
    filtered_items = []

    for item in menu_items:
        filtered_item = item.copy()

        if "children" in item:
            filtered_children = filter_menu_by_permissions(item["children"], user)

            if not filtered_children:
                continue

            filtered_item["children"] = filtered_children

        if not item["permissions"] or set(item["permissions"]).intersection(user_perms):
            filtered_items.append(filtered_item)

        elif "children" in item and filtered_item.get("children"):
            filtered_items.append(filtered_item)

    return filtered_items


def sidebar_context(request):
    """
    Menu options for sidebar
    """

    user = request.user

    cache_key = f"user-sidebar-{user.id}"
    cached_menu = cache.get(cache_key)

    if cached_menu and not settings.DEBUG:
        return {"menu": cached_menu}

    menu = [
        {
            "name": _("Inicio"),
            "url": "home",
            "icon": "bi bi-speedometer",
            "permissions": [],
            "active_children": [],
        },
        {
            "name": _("Configuración"),
            "url": "configuration",
            "icon": "bi bi-gear",
            "permissions": [],
            "active_children": [
                "profile",
                "change-password",
            ],
        },
    ]

    filtered_menu = filter_menu_by_permissions(menu, user)
    cache.set(cache_key, filtered_menu, 60 * 60 * 24)
    return {"menu": filtered_menu}


def settings_context(request):
    return {
        "version": "0.0.1",
        "site_name": "Admin",
    }
