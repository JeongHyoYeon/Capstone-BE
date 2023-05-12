from rest_framework import serializers
from .models import *


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        exclude = ['created_at', 'updated_at']