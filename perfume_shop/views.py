from distutils.log import error
from lib2to3.pgen2 import token
from django.http import JsonResponse
from .models import Perfume, PerfumeBottle, Brand, Rating, CartProduct, Cart
from .serializer import PerfumeSerializer, UserSerializer, LoinSerializer, BrandSerializer, PerfumeBottleSerializer
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

from perfume_shop import serializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView

import json


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
        print(cart.cart_products)
    elif request.method == "PUT":
        pass
    elif request.method == "DELETE":
        pass


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


@api_view(['GET'])
@permission_classes([])
def dummy_fixer(request):

    perfumes = PerfumeBottle.objects.all()
    for perfume in perfumes:
        perfume.price = round(random.uniform(500000, 20000000), 2)
        perfume.size = random.randint(100, 1000)
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


    perfume = PerfumeBottle.objects.get(id=id)
   

    serializer = PerfumeBottleSerializer(perfume, many=False)
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


@api_view(['POST'])
@permission_classes([])
def login(request):

    if request.method == 'POST':
        username = request.data.dict()['username']
        password = request.data.dict()['password']
        user = authenticate(username=username, password=password)
        data = {}
        if user is not None:
            Token.objects.get(user=user).delete()
            token = Token.objects.create(user=user)

            data['token'] = token.key
        else:
            data['error'] = "email or password is incorrect"

        return Response(data)


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

        if count is not None:
            count = int(count)
            self.pagination_class.page_size = count

        perfumes = PerfumeBottle.objects.all()
        if tester is not None:
            if tester == "false":
                perfumes = perfumes.filter(tester=False)
            elif tester == "true":
                perfumes = perfumes.filter(tester=True)

        if gender is not None and (gender == "Male" or gender == "Female"):
            perfumes = perfumes.filter(
                perfume__gender=gender)

        if brand is not None:
            perfumes = perfumes.filter(
                perfume__brand__name__contains=brand)

        if category is not None:
            perfumes = perfumes.filter(perfume__brand__category=category)

        if search is not None:
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
