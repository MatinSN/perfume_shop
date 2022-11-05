from dataclasses import field
import email
from pyexpat import model
from tkinter.ttk import Style
from rest_framework import serializers
from .models import Perfume
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


class PerfumeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Perfume
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        account = User(
            email=self.validated_data['email'],
            username=self.validated_data['username']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError(
                {'password': 'passwords must match'})

        account.set_password(password)
        account.save()
        return account


class LoinSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {

            'password': {'write_only': True}
        }


    def save(self):
        print(self.validated_data['username'])
        user = authenticate(
            username=self.validated_data['username'], password=self.validated_data['password'])
        if user is not None:
            raise serializers.ValidationError(
                {'credentials': 'email or password is incorrect'})
        else:
            token = Token.objects.create(user=user)
            return token
