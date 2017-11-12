from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.showteams, name='showteams'),
    url(r'^games/', views.showgames, name='showgames')
]