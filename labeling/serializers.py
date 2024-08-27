from django.contrib.auth.models import User, Group
from .models import Tweet
from rest_framework import serializers


class TweetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tweet
        fields = ['url', 'id_str', 'status', 'full_text', 'labels_manual',
                  'labels_automatic', 'tweet_group', 'keywords', 'content',
                  'created_at', 'updated_at', ]
