from rest_framework import serializers
from .models import *


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        exclude = ['created_at', 'updated_at']


class TagYoloSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagYolo
        fields = '__all__'


class TagFaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagFace
        fields = '__all__'


class PhotoUploadSerializer(serializers.ModelSerializer):
    tag_yolo = TagYoloSerializer(read_only=True, many=True)
    tag_face = TagFaceSerializer(read_only=True, many=True)

    class Meta:
        model = Photo
        fields = '__all__'


class PhotoReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'file_name', 'trip', 'url', 'uploaded_by', 'taken_at']