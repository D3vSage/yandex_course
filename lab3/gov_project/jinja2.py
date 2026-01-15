from django.templatetags.static import static
from django.urls import reverse
from jinja2 import Environment

def environment(**options):
    options.setdefault("extensions", [])
    options["extensions"].append("jinja2.ext.do")

    env = Environment(**options)
    env.globals.update({
        "static": static,
        "url": reverse,
    })
    return env
