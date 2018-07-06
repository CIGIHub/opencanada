from django.urls import re_path

from content_notes.views import chooser, endnotes

app_name = 'content_notes'

urlpatterns = [
    re_path(r'^choose/$', chooser.choose, name='choose'),
    re_path(r'^choose/(\d+)/$', chooser.chosen, name='chosen'),

    re_path(r'^$', endnotes.list, name='list'),
]
