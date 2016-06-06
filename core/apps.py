from django.apps import AppConfig
from django.db.models.signals import post_delete, post_save
from wagtail.wagtailsearch.backends import get_search_backends
from wagtail.wagtailsearch.index import get_indexed_instance, get_indexed_models
from wagtail.wagtailsearch.signal_handlers import post_delete_signal_handler


def post_save_signal_handler(instance, **kwargs):
    update_fields = kwargs.get('update_fields')

    social_fields = frozenset(('cached_facebook_count', 'cached_last_updated'))

    if update_fields == social_fields:
        return  # Don't update the search index if we are just updating facebook page counts

    indexed_instance = get_indexed_instance(instance)

    if indexed_instance:
        for backend in get_search_backends(with_auto_update=True):
            backend.add(indexed_instance)


def register_signal_handlers():
    # Loop through list and register signal handlers for each one
    for model in get_indexed_models():
        post_save.connect(post_save_signal_handler, sender=model)
        post_delete.connect(post_delete_signal_handler, sender=model)


class CustomWagtailSearchAppConfig(AppConfig):
    name = 'wagtail.wagtailsearch'
    label = 'wagtailsearch'
    verbose_name = "Wagtail search"

    def ready(self):
        register_signal_handlers()
