

## Installation

Run the [pip](https://pip.pypa.io/en/stable/) command to install the latest version:

```bash
   pip install git+https://github.com/sitmena/sitech-different-formset.git
```

## Usage

```bash
from sitech_different_formset import different_formset_factory
TestFormSet = different_formset_factory(Form1, Form2, {'model': User, 'fields': ['first_name', 'last_name']})
formset = TestFormSet()

############
for form in formset:
	print(form.as_table())

############
print(formset.Form1.field_name)	
print(formset.UserForm.field_name)
############
{{ form.CreateUserForm.email|as_crispy_field:"bootstrap4" }}	
	

```



    

