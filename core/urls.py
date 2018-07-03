from django.urls import re_path

from core import views

app_name = 'core'

urlpatterns = [
    re_path(r'^share/count/(?P<page_id>\d+)/$', views.social_share_count, name='social_share_count'),
]
