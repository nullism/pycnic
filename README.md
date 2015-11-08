![HUG](http://pycnic.nullism.com/images/pycnic-head-small.png)
============================

# Docs

[pycnic.nullism.com/docs](http://pycnic.nullism.com/docs)

# Example

```python
# example.py
from pycnic.core import WSGI, Handler

class Hello(Handler):
    def get(self, name="World"):
        return { "message":"Hello, %s!"%(name) }

class app(WSGI):
    routes = [
        ('/', Hello()),
        ('/([\w]+)', Hello())
    ]
```

# Installation

Now that Pycnic is available on PyPI, it may be installed with pip. 

    pip install pycnic

# Running 

Pycnic may be ran with any WSGI-compliant server, such as [Gunicorn](http://gunicorn.org).

    gunicorn file:app



