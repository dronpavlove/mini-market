from django.templatetags.static import static
from django.urls import reverse
from django.utils import translation

from jinja2 import Environment


def environment(**options):
    env = Environment(extensions=["jinja2.ext.i18n"], **options)

    env.install_gettext_translations(translation)

    for name, obj in __builtins__.items():
        if not name.startswith("_"):
            env.globals[name] = obj

    env.globals.update({
        'static': static,
        'url': reverse,
    })
    return env
