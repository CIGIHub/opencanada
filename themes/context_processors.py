from .models import get_default_theme_object


def default_theme_context(request):
    return {'default_theme': get_default_theme_object(),
            }
