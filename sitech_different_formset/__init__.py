from django.forms.utils import ErrorList, ErrorDict
from django.forms.widgets import Media
from django.utils.functional import cached_property
from django.forms import modelform_factory


def different_formset_factory(*forms):
    """Return a FormSet for the given form class."""
    form_classes = []
    for form in forms:
        if isinstance(form, dict):
            form = modelform_factory(**form)
        form_classes.append(form)
    attrs = {'form_classes': form_classes}
    return type('DifferentFormSet', (DifferentFormSet,), attrs)


class DifferentFormSet:
    """
        A collection of instances of the different Form class.
        """

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList, form_kwargs=None):
        self.is_bound = data is not None or files is not None
        self.prefix = prefix or self.get_default_prefix()
        self.auto_id = auto_id
        self.data = data or {}
        self.files = files or {}
        self.initial = initial
        self.form_kwargs = form_kwargs or {}
        self.error_class = error_class
        self._errors = None
        self._non_form_errors = None

    def __iter__(self):
        """Yield the forms in the order they should be rendered."""
        return iter(self.forms.values())

    def __getitem__(self, form_name):
        """Return the form at the given index, based on the rendering order."""
        return self.forms[form_name]

    def __len__(self):
        return len(self.forms)

    def __bool__(self):
        """
        Return True since all formsets have a management form which is not
        included in the length.
        """
        return True

    @cached_property
    def forms(self):
        """Instantiate forms at first property access."""
        forms = {}
        for form_class in self.form_classes:
            forms[form_class.__name__] = self._construct_form(form_class, **self.get_form_kwargs(form_class.__name__))
        return forms

    def get_form_kwargs(self, form_name):
        """
        Return additional keyword arguments for each individual formset form.

        index will be None if the form being constructed is a new empty
        form.
        """
        return self.form_kwargs.copy()

    def _construct_form(self, form_class, **kwargs):
        """Instantiate and return the i-th form instance in a formset."""
        defaults = {
            'auto_id': self.auto_id,
            'prefix': self.add_prefix(form_class.__name__),
            'error_class': self.error_class,
            'use_required_attribute': False,
        }
        if self.is_bound:
            defaults['data'] = self.data
            defaults['files'] = self.files
        if self.initial and 'initial' not in kwargs:
            try:
                defaults['initial'] = self.initial[form_class.__name__]
            except IndexError:
                pass
        defaults.update(kwargs)
        form = form_class(**defaults)
        return form

    @property
    def cleaned_data(self):
        """
        Return a list of form.cleaned_data dicts for every form in self.forms.
        """
        if not self.is_valid():
            raise AttributeError("'%s' object has no attribute 'cleaned_data'" % self.__class__.__name__)
        return [form.cleaned_data for form in self.forms]

    @classmethod
    def get_default_prefix(cls):
        return 'form'

    @property
    def errors(self):
        """Return a list of form.errors for every form in self.forms."""
        if self._errors is None:
            self.full_clean()
        return self._errors

    def is_valid(self):
        """Return True if every form in self.forms is valid."""
        if not self.is_bound:
            return False

        for form in self:
            if not form.is_valid():
                return False
        return True

    def full_clean(self):
        """
        Clean all of self.data and populate self._errors and
        """
        self._errors = ErrorDict()
        if not self.is_bound:  # Stop further processing.
            return

        for form in self:
            form_errors = form.errors
            self._errors.append(form_errors)
        self.clean()

    def clean(self):
        """
        Hook for doing any extra formset-wide cleaning after Form.clean() has
        been called on every form. Any ValidationError raised by this method
        will not be associated with a particular form; it will be accessible
        via formset.non_form_errors()
        """
        pass

    def has_changed(self):
        """Return True if data in any form differs from initial."""
        return any(form.has_changed() for form in self)

    def add_prefix(self, form_name):
        return '%s-%s' % (self.prefix, form_name)

    def is_multipart(self):
        """
        Return True if the formset needs to be multipart, i.e. it
        has FileInput, or False otherwise.
        """
        return any(form.is_multipart() for form in self)

    @property
    def media(self):
        """Return all media required to render the widgets on this formset."""
        media = Media()
        for form in self:
            media = media + form.media
        return media

    def as_table(self):
        "Return this formset rendered as HTML <tr>s -- excluding the <table></table>."
        return ' '.join(form.as_table() for form in self)

    def as_p(self):
        "Return this formset rendered as HTML <p>s."
        return ' '.join(form.as_p() for form in self)

    def as_ul(self):
        "Return this formset rendered as HTML <li>s."
        return ' '.join(form.as_ul() for form in self)