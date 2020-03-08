from rest_framework import serializers

from models import Names


class NamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Names
        fields = ('name', 'url')
