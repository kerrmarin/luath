from rest_framework import serializers
from .. import models

class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.List
        fields = ('list_id',
                  'list_name',
                  'distribution_list',
                  'description')

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Message
        fields = ('message_id',
                  'from_email',
                  'from_name',
                  'date',
                  'in_reply_to',
                  'subject',
                  'content',
                  'lists',
                  'references')
