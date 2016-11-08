from __future__ import unicode_literals

from django.db import models

class List(models.Model):
    list_id = models.AutoField(primary_key=True)
    list_name = models.CharField(max_length=100)
    distribution_list = models.EmailField(max_length=100)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.list_id

class Message(models.Model):
    message_id = models.CharField(max_length=200, primary_key=True)
    from_email = models.EmailField(max_length=200)
    from_name = models.CharField(max_length=200)
    date = models.DateTimeField('date sent')
    in_reply_to = models.CharField(max_length=200, null=True)
    subject = models.CharField(max_length=300)
    content = models.TextField()
    lists = models.ManyToManyField(List)
    references = models.ManyToManyField("self")

    def __str__(self):
        return self.message_id
