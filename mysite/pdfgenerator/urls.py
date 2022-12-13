from django.urls import re_path as url # update for django 4.x
from django.urls import path
from . import views


urlpatterns = [
    url(r'^$', views.landing_page, name="landing_page"),
    path('<str:category>/', views.list, name='list'),
    path('<str:category>/<str:id>/', views.form, name='form')
]
