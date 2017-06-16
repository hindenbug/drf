from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^verify/(?P<key>\w{32})/$', views.verify, name='verify'),
    url(r'^teams/$', views.create_team, name='team'),
]

