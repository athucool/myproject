from rest_framework import generics, permissions
from rest_framework import response
from rest_framework.response import Response
# from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer,UserLoginSerializer

from django.contrib.auth import login
from rest_framework import status

from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User



class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                return Response({
                "token":  token.key
                })


class LoginAPI(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not serializer.is_valid():
            try:
                pk = User.objects.get(username=serializer.data['username']).pk
            except User.DoesNotExist:
                return Response({"message": "account does not exist"}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({"message": "wrong password entered"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data['user']
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
        }, status=status.HTTP_200_OK)

