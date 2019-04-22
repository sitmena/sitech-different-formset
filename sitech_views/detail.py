from django.views.generic import DetailView as DjangoDetailView


class DetailView(DjangoDetailView):
    """A base view for displaying a single object."""
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        result = self.after_get_object()
        if result:
            return result
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def after_get_object(self):
        pass


