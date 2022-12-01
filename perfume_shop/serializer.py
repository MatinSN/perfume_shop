from dataclasses import field
import email
from pyexpat import model
from tkinter.ttk import Style
from rest_framework import serializers
from .models import Perfume, Brand, PerfumeBottle, Cart, Detail, CartProduct, Address, Rating, Comment, PaidItem, PaymentsTrackId
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


class PerfumeSerializer2(serializers.ModelSerializer):

    class Meta:
        model = Perfume
        fields = ('image',)


class PerfumeBottleSerializer2(serializers.ModelSerializer):
    perfume = PerfumeSerializer2(many=False)

    class Meta:
        model = PerfumeBottle
        fields = ('id', 'name', 'perfume',)


class PaidItemSerializer(serializers.ModelSerializer):
    product = PerfumeBottleSerializer2(many=False)

    class Meta:
        model = PaidItem
        fields = ('product', 'quantity',)


class PaymentsTrackIdSerializer(serializers.ModelSerializer):
    orders = PaidItemSerializer(many=True)

    class Meta:
        model = PaymentsTrackId
        fields = "__all__"


class UserSerializer2(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer2(many=False)

    class Meta:
        model = Comment
        fields = ('id', 'comment', 'created_at', 'user')


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detail
        fields = '__all__'


class PerfumeSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(many=False)
    details = DetailSerializer(many=True)

    class Meta:
        model = Perfume
        fields = "__all__"


class PerfumeBottleSerializer(serializers.ModelSerializer):
    perfume = PerfumeSerializer(many=False)

    class Meta:
        model = PerfumeBottle
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
        Cart.objects.create(user=account)

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


class CartProductSerializer(serializers.ModelSerializer):
    product = PerfumeBottleSerializer(many=False)

    class Meta:
        model = CartProduct
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    cart_products = CartProductSerializer(many=True)

    class Meta:
        model = Cart
        fields = ('id', 'cart_products')
