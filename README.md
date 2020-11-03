# crummycm (work in progress)

Parse config file(s) and against custom python objects.

## Example

### 1. Create a template

```python
from crummycm.validation.types.dicts.config_dict import ConfigDict as CD
from crummycm.validation.types.placeholders.placeholder import KeyPlaceholder as KPH
from crummycm.validation.types.values.element.numeric import Numeric
from crummycm.validation.types.values.element.text import Text
from crummycm.validation.types.values.element.bool import Bool
from crummycm.validation.types.values.compound.multi import Multi


ACCEPTED_DTYPES = ["int32", "float32", "int64", "float64"]

TEMPLATE = {
        "data": {
            "name": Text(required=True, to_lower=True),
            "schema": {
                KPH(name="feature_name", multi=True, required=True): {
                    "shape": Multi(
                        required=True, is_type=list, element_types=Numeric(is_type=int)
                    ),
                    "dtype": Text(required=True, is_in_list=ACCEPTED_DTYPES),
                    KPH("label", exact=True, required=False): Bool(required=True),
                }
            },
            "source": Text(required=True, starts_with="http:"),
        }
    }

```

### 1a (optional) Generate template to fill in

```python
import crummycm as ccm

ccm.template(TEMPLATE, "<path>/main.yml")
```

```yaml
data:
  name: '[Text]*'
  schema:
    MULTI:[KPH]*:
      '[True]': '[Bool]*'
      dtype: '[Text]^*'
      shape: '[list] of el:<class ''int''>[Numeric]*[Multi]*'
  source: '[Text]^*'
```
> note: the above schematics are likely going to change. Right now KPH =
> KeyPlaceholder(), * = required, MULTI:xx = there might be many here, ^ = there
> are some requirements for the value (starts_with, ends_with, etc) (view the
> template to see them), ! = a fn is applied, and () = the default value. in
> `shape` above '[list] of el:<class ''int''>[Numeric]*[Multi]*' means there is
> a list of elements of type Numeric (int type) and there may be many (yeah, I
> agree it's hard to read, I think this will change in the future)

### 2. Create config Files
The configuration files can be one of multiple formats.

`<path>/main.yml`

NOTE: the `::` in the `schema` line designates an instruction (function) that is
to be called on the given input. In this case the instruction is `parse_path`
found in `crummycm/src/crummycm/read/key_instructions/functions/standard.py`
```yaml
data:
  name: "MNIST"
  schema: "parse_path::./tests/integration/example_files/example/schema.json"
  source: "http://yann.lecun.com/exdb/mnist/"
```

`<path>/schema.json`
```json
{
    "x_image": {
        "shape": [
            28,
            28,
            1
        ],
        "dtype": "float32"
    },
    "y_target": {
        "shape": [
            1,
            1
        ],
        "dtype": "int32",
        "label": true
    }
}
```


### 3. Read+Validate
```python
import crummycm as ccm

my_config = ccm.generate(user_in="<path>/main.yml", template=TEMPLATE)
```
This will read the user input described in `"<path>/main.yml"` and validate the
input against the template (e.g. `TEMPLATE`)


```python
print(my_config)
```
```python
{
    "data": {
        "name": "mnist",
        "schema": {
            "x_image": {"shape": [28, 28, 1], "dtype": "float32"},
            "y_target": {"shape": [1, 1], "dtype": "int32", "label": True},
        },
        "source": "http://yann.lecun.com/exdb/mnist/",
    }
}
```

### 4. Use your config (`my_config`)

```python
out = some_program(my_config)
```