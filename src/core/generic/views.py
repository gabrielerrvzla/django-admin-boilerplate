from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, FormView, ListView, UpdateView
from django_filters import FilterSet


class GenericListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = "generic/list.html"
    context_object_name = "objects"
    paginate_by = 10
    filterset: FilterSet | None = None
    actions: list[dict] = []
    columns: list[dict] = []
    columns_actions: list[dict] = []

    def dispatch(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.filterset:
            return self.filterset(self.request.GET, queryset=queryset).qs

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.filterset:
            context["filterset"] = self.filterset(self.request.GET, queryset=self.object_list)

        if self.actions:
            context["actions"] = self._process_actions(self.actions)

        if self.columns:
            context["columns"] = self.columns

        if self.columns_actions:
            context["columns_actions"] = True
            context["objects"] = self._process_columns_actions(context["objects"])

        return context

    def get_paginate_by(self, queryset):
        paginate_by = self.request.GET.get("paginate_by", self.paginate_by)

        if paginate_by:
            if paginate_by in ["10", "25", "50", "100"]:
                return int(paginate_by)

        return super().get_paginate_by(queryset)

    def _process_actions(self, actions):
        return [action for action in actions if self.request.user.has_perm(action["permission"])]

    def _process_columns_actions(self, object_list):
        object_list_with_actions = []

        for obj in object_list:
            obj.actions = [
                {
                    **action,
                    "url": (action["url"](obj) if callable(action["url"]) else action["url"]),
                }
                for action in self.columns_actions
                if self.request.user.has_perm(action["permission"])
                and ("condition" not in action or action["condition"](obj))
            ]
            object_list_with_actions.append(obj)

        return object_list_with_actions


class GenericFormView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, FormView):
    template_name = "generic/form.html"
    success_message = _("Acción realizada correctamente.")


class GenericCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "generic/form.html"
    success_message = _("Acción realizada correctamente.")


class GenericUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = "generic/form.html"
    success_message = _("Acción realizada correctamente.")


class GenericDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = "generic/delete.html"
    success_message = _("Acción realizada correctamente.")
