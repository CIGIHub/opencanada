from django.conf.urls import url

from core import views

app_name = 'core'

urlpatterns = [
    url(r'^share/count/(?P<page_id>\d+)/$', views.social_share_count, name='social_share_count'),
]
