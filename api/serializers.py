from rest_framework import serializers

from invoices import models


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Item
        fields = ['id', 'name', 'description', 'price']
