from django.conf.urls import url, handler404
from views import home

urlpatterns = [
    url(r'^$', home.index, name='index')
]

handler404 = 'luath_site.views.error.not_found'
