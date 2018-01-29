from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.showteams, name='showteams'),
    url(r'^games/(?P<season>\d{4})/week/(?P<week>\d+)', views.showgames, name='showgames'),
    url(r'^picks/', views.makepicks, name='makepicks'),
    url(r'^picks/(?P<id>\d+)', views.storepick, name='storepick'),
    url(r'^api/update/json/(?P<season>\d{4})/(?P<week>\d+)', views.updategames, name='updategames'),
    url(r'^user/', include('django.contrib.auth.urls'))
]