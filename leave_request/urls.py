from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^actions/', views.actions, name='actions'),
    url(r'^reject/', views.reject, name='reject'),
    url(r'^reject/(?P<reject_id>\d+)/$', views.reject, name='reject'),
]
