from distutils.log import error
from lib2to3.pgen2 import token
from django.http import JsonResponse
from .models import Perfume, PerfumeBottle
from .serializer import PerfumeSerializer, UserSerializer, LoinSerializer
from .helpers import men_filter
import operator
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User, auth
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from perfume_shop import serializer


def temp(x):
    if x.perfume.sex == "female":
        return True
    else:
        return False


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def men_perfume(request):
    perfumes = filter(men_filter, Perfume.objects.all())
    print(list(filter(temp, PerfumeBottle.objects.all())))
    perfumes = sorted(perfumes, key=operator.attrgetter('price'), reverse=True)

    serializer = PerfumeSerializer(perfumes, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(["POST"])
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
