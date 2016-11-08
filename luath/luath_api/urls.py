from django.conf.urls import url, include
from rest_framework import routers
from . import views
from viewsets import viewsets

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'', viewsets.ListViewSet)
router.register(r'(?P<list_id>[0-9]+)/messages', viewsets.MessageViewSet)

urlpatterns = [
    url(r'^v1/lists/', include(router.urls)),
]
