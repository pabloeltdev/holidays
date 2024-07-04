from django.contrib.auth.models import Group, User
from rest_framework import serializers
from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'username', 'email', 'groups']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['pk', 'name']


class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Holiday
        fields = ['pk', 'title', 'description', 'country', 'event_day',
                  'image', 'event_month', 'event_long_month']
