import traceback
from pathlib import Path
import os
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import timedelta
from random import randrange
from distutils.log import error
from lib2to3.pgen2 import token
from django.http import JsonResponse
from .models import Perfume, PerfumeBottle, Brand, Rating, Cart, CartProduct, PaymentsTrackId, Address, Comment, PaidItem
from .serializer import PerfumeSerializer, UserSerializer, LoinSerializer, BrandSerializer, PerfumeBottleSerializer, CartSerializer, AddressSerializer, RatingSerializer, CommentSerializer, PaymentsTrackIdSerializer
from .helpers import men_filter
import operator
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User, auth
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import random
from django.db.models import Q
import datetime
from .utils import add_item_to_cart, delete_cart_item
from perfume_shop import serializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from urllib.request import urlopen
from django.http import HttpResponse

import json
import math
import requests
import datetime


def temp(x):
    if x.perfume.sex == "female":
        return True
    else:
        return False


@api_view(['DELETE', 'PUT', 'GET'])
@permission_classes((IsAuthenticated,))
def cart(request):
    cart = Cart.objects.filter(user=request.user)
    if request.method == "GET":
        serializer = CartSerializer(cart[0], many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        product_id = request.query_params.get("product_id")
        quantity = request.query_params.get("quantity")
        return add_item_to_cart(quantity=quantity, product_id=product_id, user_cart=cart[0])

    elif request.method == "DELETE":
        quantity = request.query_params.get("quantity")
        product_id = request.query_params.get("product_id")

        return delete_cart_item(quantity=quantity, product_id=product_id, user_cart=cart[0])


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def cart_check(request):
    request_cart = json.loads(request.data["cart"])
    user_cart = Cart.objects.get(user=request.user)
    for item in request_cart:
        try:
            perfume = PerfumeBottle.objects.get(id=item["id"])
        except:
            return Response({"message": "Perfume not found"})
        try:
            cart_item = CartProduct.objects.get(
                cart=user_cart, product=perfume)
            if item["quantity"] > cart_item.quantity:

                return add_item_to_cart(product_id=item["id"], quantity=item["quantity"]-cart_item.quantity, user_cart=user_cart)
            if item["quantity"] < cart_item.quantity:

                return delete_cart_item(product_id=item["id"], quantity=cart_item.quantity-item["quantity"], user_cart=user_cart)

        except:
            return add_item_to_cart(product_id=item["id"], quantity=item["quantity"], user_cart=user_cart)

    return Response()


@api_view(['GET'])
@permission_classes([])
def brands(request):
    # category = request.GET['category']
    category = None
    if 'category' in request.query_params:
        category = request.query_params['category']

    brands = Brand.objects.filter(
        category=category) if category != None else Brand.objects.all()
    serializer = BrandSerializer(brands, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


def random_date(start, end):
    """
    This function will return a random datetime between two datetime 
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


@api_view(['GET'])
@permission_classes([])
def dummy_fixer(request):

    perfumes = PerfumeBottle.objects.all()

    d1 = datetime.datetime.strptime('1/1/2020 1:30 PM', '%m/%d/%Y %I:%M %p')
    d2 = datetime.datetime.strptime('1/1/2022 4:50 AM', '%m/%d/%Y %I:%M %p')
    BASE_DIR = Path(__file__).resolve().parent.parent
    for perfume in perfumes:
        perfume.price = round(random.uniform(800000, 20000000), 2)
        perfume.size = random.randint(200, 700)
        perfume.rate = random.randint(0, 5)
        perfume.discount = random.randint(0, 60)
        perfume.created_at = random_date(d1, d2)

        perfume.save()
        perfume.image = "perfumes/p3.jpg"
        perfume.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([])
def temp_rater(request):

    perfumes = PerfumeBottle.objects.all()
    for perfume in perfumes:
        print(perfume)
        ratings = Rating.objects.filter(perfume=perfume)
        rate = 0
        for rating in ratings:
            rate = rate + rating.rating
        if len(ratings) > 0:
            rate = rate/len(ratings)
        perfume.rate = rate
        perfume.save()
    return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([])
def men_perfume(request):
    perfumes = filter(men_filter, Perfume.objects.all())
    print(list(filter(temp, PerfumeBottle.objects.all())))
    perfumes = sorted(perfumes, key=operator.attrgetter('price'), reverse=True)

    serializer = PerfumeSerializer(perfumes, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(["GET"])
@permission_classes([])
def get_perfume(request, id):

    perfume = PerfumeBottle.objects.filter(id=id)

    if len(perfume) == 0:
        return Response({"message": "Could not find the perfume"}, status=status.HTTP_404_NOT_FOUND)

    serializer = PerfumeBottleSerializer(perfume[0], many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([])
def signup(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)

        data = {}

        if serializer.is_valid():

            account = serializer.save()
            data['response'] = "Account has been created successfully"
            data['username'] = account.username
            data['email'] = account.email
            token = Token.objects.get(user=account)
            data['token'] = token.key

        else:
            data = serializer.errors

        return Response(data)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated, ])
def address(request):

    if request.method == "GET":
        user_addresses = Address.objects.filter(user=request.user)
        serializer = AddressSerializer(user_addresses, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        name = request.data["name"]
        lastname = request.data["lastname"]
        state = request.data["state"]
        city = request.data["city"]
        address = request.data["address"]
        phone_number = request.data["phone_number"]
        new_address = Address.objects.create(user=request.user,
                                             name=name, lastname=lastname, state=state, city=city, address=address, phone_number=phone_number)
        serializer = AddressSerializer(new_address, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([])
def login(request):

    if request.method == 'POST':
        print(request.data)
        username = request.data['username']
        password = request.data['password']

        

        user = authenticate(username=username, password=password)
        data = {}
        if user is not None:
            Token.objects.get(user=user).delete()
            token = Token.objects.create(user=user)

            data['token'] = token.key
            data['username'] = user.get_username()
            logged_in_user = User.objects.get(username=data['username'])
            data['email'] = logged_in_user.email
            return Response(data)

        else:
            data['error'] = "username or password is incorrect"
            return Response(data, status=status.HTTP_404_NOT_FOUND)


class BrandListView(ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    authentication_classes = []
    permission_classes = []
    pagination_class = PageNumberPagination

    def get_queryset(self):

        brand_type = self.request.query_params.get('brand_type')
        count = self.request.query_params.get('count')
        brands = Brand.objects.all()
        print("Here for category")

        if count is not None:
            count = int(count)
            self.pagination_class.page_size = count
        if brand_type is not None:
            brands = brands.filter(category=brand_type)

        return brands


class PerfumeListView(ListAPIView):
    queryset = PerfumeBottle.objects.all()
    serializer_class = PerfumeBottleSerializer
    authentication_classes = []
    permission_classes = []
    pagination_class = PageNumberPagination

    def brand_name_filter(perfume, brand_name):
        if perfume.brand.name == brand_name:
            return True
        else:
            return False

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """

        gender = self.request.query_params.get('gender')
        tester = self.request.query_params.get('tester')
        brand = self.request.query_params.get('brand')
        category = self.request.query_params.get('category')
        search = self.request.query_params.get('search')
        price_sort_dec = self.request.query_params.get('price_sort_dec')
        price_sort_ace = self.request.query_params.get('price_sort_ace')
        date_sort = self.request.query_params.get('date_sort')
        count = self.request.query_params.get('count')
        rate_sort = self.request.query_params.get('rate_sort')
        big_size = self.request.query_params.get('big_zige')

        if count is not None:
            count = int(count)
            self.pagination_class.page_size = count

        perfumes = PerfumeBottle.objects.all()

        if big_size is not None and big_size == "true":
            perfumes = perfumes.filter(size__gte=100)

        if tester is not None and tester != "Both":
            if tester == "false":
                perfumes = perfumes.filter(tester=False)
            elif tester == "true":
                perfumes = perfumes.filter(tester=True)

        if gender is not None and (gender == "Male" or gender == "Female"):
            perfumes = perfumes.filter(
                perfume__gender=gender)

        if brand is not None and brand != "":
            perfumes = perfumes.filter(
                perfume__brand__name__contains=brand)

        if category is not None:
            perfumes = perfumes.filter(perfume__brand__category=category)

        if search is not None and search != "":
            perfumes = perfumes.filter(
                Q(perfume__name__contains=search) | Q(perfume__brand__name__contains=search))

        if price_sort_dec is not None and price_sort_dec == "true":
            perfumes = perfumes.order_by("-price")
        elif price_sort_ace is not None and price_sort_ace == "true":
            perfumes = perfumes.order_by("price")
        elif date_sort is not None and date_sort == "true":
            perfumes = perfumes.order_by("-created_at")
        elif rate_sort is not None and rate_sort == "true":
            print("Here of the rate sort")
            perfumes = perfumes.order_by("-rate")

        return perfumes


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def payment_request(request):
    cart = Cart.objects.get(user=request.user)
    address_data = json.loads(request.data["address"])

    cart_products = CartProduct.objects.filter(cart=cart)

    if len(cart_products) > 0:
        payment_description = {}
        payment = 0
        c = 1
        for cart_product in cart_products:
            print(cart_product.product.perfume.name)
            payment_description[str(c)+"-"+cart_product.product.perfume.name] = " X " + str(cart_product.quantity) + " " +    \
                "with the base price of " + str(cart_product.product.price)
            payment = payment + (cart_product.quantity * math.trunc(
                (cart_product.product.price*((100-cart_product.product.discount)/100))))
            c = c+1
        myobj = {
            "merchant": "zibal",
            "amount": payment * 10,
            "callbackUrl": "http://127.0.0.1:3000/callback/",
            "description": json.dumps(payment_description),

        }
        response = requests.post(
            "https://gateway.zibal.ir/v1/request", json=myobj)
        responseDict = json.loads(response.text)
        print(response.text)
        if responseDict["result"] == 100:
            shipping_address = Address.objects.create(
                user=request.user, name=address_data["name"],
                lastname=address_data["lastName"], state=address_data["state"],
                city=address_data["city"], address=address_data["address"],
                phone_number=address_data["phoneNumber"])
            PaymentsTrackId.objects.create(
                trackId=responseDict["trackId"], user=request.user, shipping_info=shipping_address, status="Not Paid", amount=payment)
            return Response({"trackId": responseDict["trackId"]}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Could not process your payment"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        return Response({"message": "There no product in your cart!"})


@api_view(['GET'])
@permission_classes([])
def payment_callback(request):
    success = request.query_params.get('success')
    trackId = request.query_params.get('trackId')

    if success is not None:

        if success == "1":

            if trackId is not None:

                myobj = {
                    "merchant": "zibal",
                    "trackId": int(trackId)
                }
                response = requests.post(
                    "https://gateway.zibal.ir/v1/verify", json=myobj)
                responseDict = json.loads(response.text)
                if responseDict['result'] == 100 and responseDict['status'] == 1:
                    payment_track_id = PaymentsTrackId.objects.get(
                        trackId=trackId)
                    if payment_track_id.status == "Not Paid":
                        payment_track_id.status = "Processing"
                        paid_date = datetime.datetime.strptime(
                            responseDict["paidAt"], '%Y-%m-%dT%H:%M:%S.%f')
                        payment_track_id.payment_date = paid_date
                        payment_track_id.save()
                        cart = Cart.objects.get(user=payment_track_id.user)
                        cart_products = CartProduct.objects.filter(cart=cart)

                        for cart_product in cart_products:
                            PaidItem.objects.create(
                                product=cart_product.product, payment=payment_track_id, quantity=cart_product.quantity)
                        cart_products.delete()
                    return Response({"message:payment was successful"},
                                    status=status.HTTP_200_OK)

    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def orders(request):

    paid_orders = PaymentsTrackId.objects.filter(user=request.user)
    paid_orders = paid_orders.filter(
        Q(status='Processing') | Q(status="Sent") | Q(status="Received"))
    paid_orders = paid_orders.order_by("-payment_date")

    serializer = PaymentsTrackIdSerializer(paid_orders, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, ])
def rate_perfume(request):

    product_id = request.query_params.get('product_id')
    perfumes = PerfumeBottle.objects.filter(id=product_id)
    if len(perfumes) == 0:
        return Response({"message": "There is no such perfume with this id"}, status=status.HTTP_404_NOT_FOUND)
    perfume = perfumes[0]

    if request.method == "GET":

        ratings = Rating.objects.filter(user=request.user, perfume=perfume)
        if len(ratings) == 0:
            return Response({"rating": 0}, status=status.HTTP_404_NOT_FOUND)

        rating = ratings[0]

        return Response({"rating": rating.rating}, status=status.HTTP_200_OK)

    elif request.method == "POST":

        rating = request.data.get('rating')

        if rating == None:
            return Response({"message": "rating must be provided"}, status=status.HTTP_400_BAD_REQUEST)
        user_pre_rating = Rating.objects.filter(
            user=request.user, perfume=perfume)

        if len(user_pre_rating) == 0:
            Rating.objects.create(rating=int(
                rating), user=request.user, perfume=perfume)
        else:
            print("Here for changing the pre rating")
            user_pre_rating[0].rating = int(rating)
            user_pre_rating[0].save()

        perfume_ratings = Rating.objects.filter(perfume=perfume)

        sum = 0
        for rate in perfume_ratings:
            sum = sum + rate.rating
        perfume.rate = round(sum/len(perfume_ratings))
        perfume.save()

        newRating = Rating.objects.get(user=request.user, perfume=perfume)

        serializer = RatingSerializer(newRating, many=False)

        print("rating", rating)
        return Response({"comment": serializer.data, "perfume_rating": perfume.rate}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([])
def perfume_comments(request):

    product_id = request.query_params.get('product_id')
    perfumes = PerfumeBottle.objects.filter(id=product_id)
    if len(perfumes) == 0:
        return Response({"message": "There is no such perfume with this id"}, status=status.HTTP_404_NOT_FOUND)
    perfume = perfumes[0]

    if request.method == "GET":
        perfume_comments = Comment.objects.filter(perfume=perfume)
        perfume_comments = perfume_comments.order_by("-created_at")
        serializer = CommentSerializer(perfume_comments, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def add_comment(request):

    product_id = request.query_params.get('product_id')
    perfumes = PerfumeBottle.objects.filter(id=product_id)
    if len(perfumes) == 0:
        return Response({"message": "There is no such perfume with this id"}, status=status.HTTP_404_NOT_FOUND)
    perfume = perfumes[0]

    if request.method == "POST":
        comment = request.data.get("comment")
        if comment is None:
            return Response({"massage": "comment must be provided"}, status=status.HTTP_400_BAD_REQUEST)
        new_comment = Comment.objects.create(
            user=request.user, perfume=perfume, comment=comment)
        serializer = CommentSerializer(new_comment, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)
