from django.views.generic import ListView as DjangoListView
from django.views.generic.edit import FormMixin


class ListView(DjangoListView, FormMixin):
    """
    Render some list of objects, set by `self.model` or `self.queryset`.
    `self.queryset` can actually be any iterable of items, not just a queryset.
    """
    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        form = None
        if form_class is None:
            form_class = self.get_form_class()
        if form_class is not None:
            form = form_class(**self.get_form_kwargs())
        return form

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
        }

        kwargs.update({
            'data': self.request.GET,
        })
        return kwargs

