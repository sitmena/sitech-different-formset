from django.views.generic import (
    View as DjangoView, RedirectView as DjangoRedirectView,
    TemplateView as DjangoTemplateView
)


class View(DjangoView):
    """
    Intentionally simple parent class for all views. Only implements
    dispatch-by-method and simple sanity checking.
    """


class RedirectView(DjangoRedirectView):
    """Provide a redirect on any GET request."""


class TemplateView(DjangoTemplateView):
    """
    Render a template. Pass keyword arguments from the URLconf to the context.
    """