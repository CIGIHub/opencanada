from django.conf.urls import url

from content_notes.views import chooser, endnotes

app_name = 'content_notes'

urlpatterns = [
    url(r'^choose/$', chooser.choose, name='choose'),
    url(r'^choose/(\d+)/$', chooser.chosen, name='chosen'),

    url(r'^$', endnotes.list, name='list'),
]
