from django.views.generic import (
    DeleteView as DjangoDeleteView, UpdateView as DjangoUpdateView,
    CreateView as DjangoCreateView, FormView as DjangoFormView, View
)
from collections import OrderedDict
from django.views.generic.edit import BaseUpdateView
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateResponseMixin, ContextMixin
from django.core.exceptions import ImproperlyConfigured


class MultipleFormMixin(ContextMixin):
    """Provide a way to show and handle a form in a request."""
    initial = {}
    form_classes = None
    success_url = None

    def __init__(self, *args, **kwargs):
        self.form_classes = OrderedDict(self.form_classes)
        return super().__init__(*args, **kwargs)

    def get_initial(self, name):
        """
        Returns the initial data to use for forms on this view.
        """
        self.initial.setdefault(name, {})
        return self.initial[name].copy()

    def get_prefix(self, name):
        """Return the prefix to use for forms."""
        return name

    def get_form_class(self, name):
        """
        Returns the form class to use in this view
        """
        return self.form_classes[name]

    def get_form_kwargs(self, name):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = {
            'initial': self.get_initial(name),
            'prefix': self.get_prefix(name),
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_form(self, name, form_class=None):
        """
        Returns an instance of the form to be used in this view.
        """
        if form_class is None:
            form_class = self.get_form_class(name)
        return form_class(**self.get_form_kwargs(name))

    def get_forms(self, names=None, form_classes=None):
        if names is None:
            names = self.form_classes.keys()

        if form_classes is None:
            form_classes = {}

        return OrderedDict(
            [(name, self.get_form(name, form_classes.get(name, None)))
             for name in names]
        )

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        if not self.success_url:
            raise ImproperlyConfigured("No URL to redirect to. Provide a success_url.")
        return str(self.success_url)  # success_url may be lazy

    def forms_valid(self, forms):
        """If the form is valid, redirect to the supplied URL."""
        return HttpResponseRedirect(self.get_success_url())

    def forms_invalid(self, forms):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(forms=forms))

    def get_context_data(self, **kwargs):
        """Insert the forms into the context dict."""
        if 'forms' not in kwargs:
            kwargs['forms'] = self.get_forms()
        return super().get_context_data(**kwargs)


class ProcessMultipleFormsView(View):
    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        forms = self.get_forms()
        if all(form.is_valid() for form in forms.values()):
            return self.forms_valid(forms)
        else:
            return self.forms_invalid(forms)

    # PUT is a valid HTTP verb for creating (with a known URL) or editing an
    # object, note that browsers only support POST for now.
    def put(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class BaseMultipleFormView(MultipleFormMixin, ProcessMultipleFormsView):
    """
    A base view for displaying a heterogeneous set of forms.
    """


class MultipleFormView(TemplateResponseMixin, BaseMultipleFormView):
    """
    A view for displaying a heterogeneous set of forms and rendering a template response.
    """


class FormView(DjangoFormView):
    """A view for displaying a form and rendering a template response."""


class CreateView(DjangoCreateView):
    """
    View for creating a new object, with a response rendered by a template.
    """


class UpdateView(DjangoUpdateView):
    """View for updating an object, with a response rendered by a template."""
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        result = self.after_get_object()
        if result:
            return result
        return super(BaseUpdateView).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        result = self.after_get_object()
        if result:
            return result
        return super(BaseUpdateView).post(request, *args, **kwargs)

    def after_get_object(self):
        pass


class DeleteView(DjangoDeleteView):
    """
    View for deleting an object retrieved with self.get_object(), with a
    response rendered by a template.
    """
    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        result = self.after_get_object()
        if result:
            return result
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

    def after_get_object(self):
        pass
