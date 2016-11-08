from rest_framework import viewsets
from .. import models
from ..serializers import serializers
from rest_framework.permissions import IsAuthenticated

# ViewSets define the view behavior.
class ListViewSet(viewsets.ModelViewSet):
    queryset = models.List.objects.all()
    serializer_class = serializers.ListSerializer
    http_method_names = ['get']
    permission_classes = [IsAuthenticated]

# ViewSets define the view behavior.
class MessageViewSet(viewsets.ModelViewSet):
    queryset = models.Message.objects.all()
    serializer_class = serializers.MessageSerializer
    http_method_names = ['get']
    lookup_value_regex = '.+'
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        list_id = self.kwargs['list_id']
        return models.Message.objects.filter(lists__list_id=list_id).order_by('-date')
