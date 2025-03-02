import django_filters
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from .models import User


class UserFilterset(django_filters.FilterSet):
    search = django_filters.CharFilter(
        label=_("Buscar"),
        method="search_filter",
    )

    is_active = django_filters.ChoiceFilter(
        label=_("Estado"),
        choices=[
            ("True", _("Activo")),
            ("False", _("Inactivo")),
        ],
    )

    class Meta:
        model = User
        fields = [
            "search",
            "is_active",
        ]

    def search_filter(self, queryset, name, value):
        """
        Filter by first_name, last_name and email.
        """

        terms = value.split()

        query = Q()
        for term in terms:
            query &= Q(full_name__icontains=term) | Q(email__icontains=term)

        return queryset.filter(query)
