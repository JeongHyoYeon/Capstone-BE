from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


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
