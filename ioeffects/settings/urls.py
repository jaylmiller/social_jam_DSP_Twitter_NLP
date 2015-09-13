from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^/submit/$', views.submit, name='submit'),
        url(r'examine/', views.examine, name='examine'),
]
