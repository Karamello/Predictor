from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.showteams, name='showteams'),
    url(r'^games/(?P<season>\d{4})/week/(?P<week>\d+)', views.showgames, name='showgames'),
    url(r'^picks/', views.makepicks, name='makepicks'),
    url(r'^api/update/json', views.updategames, name='updategames')
]