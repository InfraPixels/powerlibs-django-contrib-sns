# powerlibs-django-contrib-sns

[![CircleCI](https://circleci.com/gh/DroneMapp/powerlibs-django-contrib-sns/tree/master.svg?style=svg)](https://circleci.com/gh/DroneMapp/powerlibs-django-contrib-sns/tree/master)

SNS integration for Django models

## CRUDNotifierMixin

Sends messages to `<model-name-snakecased>__<CRUD-operation>`
containing the serialized version of the full object.


```python
from django.db import models
from powerlibs.django.contrib.sns.models import CRUDNotifierMixin


class MyModel(CRUDNotifierMixin, models.Model):
    name = models.CharField(max_length=64)
```


Resultant topics:

 * POST -> `my_model__created`
 * PUT/PATH -> `my_model__updated`
 * DELETE -> `my_model__deleted`


### ChangeNotifierMixin

Sends messages to `<model-name-snakecased>__<field>__<value>`
(or `<model-name-snakecased>__<value>` if `field == "status"`
containing the serialized version of the full object.

By default, uses `["status"]` as "notable fields", that is,
the model's fields that should be monitored for changes. You
can customize it by defining a `notable_fields' attribute on
the model.

```python
from django.db import models
from powerlibs.django.contrib.sns.models import CRUDNotifierMixin


class MyModel(ChangeNotifierMixin, models.Model):
    name = models.CharField(max_length=64)
    status = models.CharField(max_length=16, choices=(
        ('new', 'new'),
        ('processing', 'processing'),
        ('finished', 'finished'),
    ))
    step = models.IntegerField()
```


Resultant topics:

 * `my_model__new` when the object is created (and saved) or
 the `status` is changed to "new".
 * `my_model__step__1` when the `step` field is changed to 1.


It can work side-by-side with CRUDNotifierMixin.
