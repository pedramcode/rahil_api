from rest_framework import serializers
from .models import Item


class ItemModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ['name']
