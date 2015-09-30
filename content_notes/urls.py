from django.conf.urls import url

from content_notes.views import chooser, endnotes

urlpatterns = [
    url(r'^choose/$', chooser.choose, name='choose'),
    url(r'^choose/(\d+)/$', chooser.chosen, name='chosen'),

    url(r'^/$', endnotes.list, name='list'),
]
