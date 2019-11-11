
#  Sitech-different-formset
A formset is a layer of abstraction to work with diffrent forms on the same page.

### Installation

Run the [pip](https://pip.pypa.io/en/stable/) command to install the latest version:

```bash
   pip install git+https://github.com/sitmena/sitech-different-formset.git@v1.0
```

### Usage

```python
# in views.py
from sitech_different_formset import different_formset_factory

TestFormSet = different_formset_factory(Form1, Form2, {'model': User, 'fields': ['field1_name', 'field2_name']})
formset = TestFormSet(request.POST, initil={'Form1': ..., 'UserForm': ...}, instances={'UserForm': ...} )

for form in formset:
	print(form.as_table())


print(formset.Form1)	
print(formset.UserForm)


# in template.html
{{ formset.Form1.field_name|as_crispy_field:"bootstrap4" }}		
{{ formset.UserForm.field_name|as_crispy_field:"bootstrap4" }}
```



    

