from __future__ import absolute_import, unicode_literals

import json

from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from wagtail.wagtailadmin.widgets import AdminChooser

from articles.models import EndNote


class AdminEndNoteChooser(AdminChooser):
    target_content_type = None

    def __init__(self, **kwargs):

        snippet_type_name = "End Note"
        self.choose_one_text = _('Choose %s') % snippet_type_name
        self.choose_another_text = _('Choose another %s') % snippet_type_name
        self.link_to_chosen_text = _('Edit this %s') % snippet_type_name

        super(AdminEndNoteChooser, self).__init__(**kwargs)

    def render_html(self, name, value, attrs):
        # model_class = EndNote

        instance = EndNote.objects.get(uuid=value)
        value = instance.uuid
        # instance, value = self.get_instance_and_id(model_class, value)

        original_field_html = super(AdminEndNoteChooser, self).render_html(name, value, attrs)

        return render_to_string("content_notes/end_note_chooser.html", {
            'widget': self,
            'original_field_html': original_field_html,
            'attrs': attrs,
            'value': value,
            'item': instance,
        })

    def render_js_init(self, id_, name, value):
        return "createEndNoteChooser({id});".format(
            id=json.dumps(id_))
