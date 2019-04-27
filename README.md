
## Installation

Run the [pip](https://pip.pypa.io/en/stable/) command to install the latest version:

```bash
   pip install git+https://github.com/sitmena/sitech-different-formset.git
```

## Usage

```bash
from sitech_different_formset import different_formset_factory
TestFormSet = different_formset_factory(Form1, Form2, Form3)
formset = TestFormSet()

for form in formset:
	print(form.as_table())

```


