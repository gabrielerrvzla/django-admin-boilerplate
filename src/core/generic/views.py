from datetime import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, FormView, ListView, UpdateView, View
from django_filters import FilterSet
from import_export.formats.base_formats import DEFAULT_FORMATS
from import_export.resources import ModelResource


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


class GenericExportView(LoginRequiredMixin, PermissionRequiredMixin, View):
    resource_class: ModelResource
    format: str = "csv"
    filterset: FilterSet | None = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not hasattr(self.resource_class, "_meta"):
            raise ValueError(_("El recurso debe tener un atributo _meta definido."))
        self.model = self.resource_class._meta.model

    def get_supported_formats(self):
        return {fmt().get_title(): fmt for fmt in DEFAULT_FORMATS}

    def get_filter_params(self):
        refer = self.request.headers.get("Referer")
        if not refer:
            return {}

        query_string = refer.split("?")[-1]
        filters = {}

        for param in query_string.split("&"):
            try:
                key, value = param.split("=")
                if key in self.filterset.base_filters:
                    filters[key] = value
            except ValueError:
                continue

        return filters

    def get_queryset(self):
        if self.filterset:
            filters = self.get_filter_params()
            return self.filterset(filters, queryset=self.model.objects.all()).qs
        return self.model.objects.all()

    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if not queryset.exists():
            messages.warning(request, _("No hay elementos para exportar."))
            referer = request.headers.get("Referer", "/")
            return redirect(referer)

        supported_formats = self.get_supported_formats()
        export_format = self.format.lower()

        if export_format not in supported_formats:
            messages.error(request, _("Formato no soportado."))
            return redirect(request.headers.get("Referer", "/"))

        resource = self.resource_class()
        dataset = resource.export(queryset)
        format_class = supported_formats[export_format]()

        file_data = format_class.export_data(dataset)
        content_type = format_class.get_content_type()

        response = HttpResponse(file_data, content_type=content_type)
        filename = self.get_filename(export_format)
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response

    def get_filename(self, export_format: str) -> str:
        filename = self.model._meta.verbose_name_plural.replace(" ", "_").lower()
        date = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        return f"{filename}-{date}.{export_format}"
