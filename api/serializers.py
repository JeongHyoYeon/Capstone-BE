from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class UserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroup
        fields = '__all__'


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
        fields = ['id', 'trip', 'url', 'uploaded_by', 'taken_at']


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']

    def create(self, validated_data):
        id = validated_data.get('id')
        name = validated_data.get('name')
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = User(
            id=id,
            name=name,
            email=email
        )
        user.set_password(password)
        user.save()
        return user
