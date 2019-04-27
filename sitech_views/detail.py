from django.views.generic import DetailView as DjangoDetailView


class DetailView(DjangoDetailView):
    """A base view for displaying a single object."""
    def get(self, request, *args, **kwargs):
        before_get_object = self.before_get_object()
        if before_get_object:
            return before_get_object
        self.object = self.get_object()
        after_get_object = self.after_get_object()
        if after_get_object:
            return after_get_object
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def before_get_object(self):
        pass

    def after_get_object(self):
        pass


