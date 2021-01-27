from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import socket
from django.db.models.signals import pre_save,post_save
from django.shortcuts import redirect





class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return user

class UserLoginSerializer(serializers.Serializer):
    username=serializers.CharField(max_length=128)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    def validate(self, data):
        username=data.get('username', None)
        password = data.get("password", None)
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )
        return user




def post_save_session_reciver(sender,instance,created,*args, **kwargs):
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    d={"user": instance.id,'ip':ip_address}
    if created:
        return redirect("https://encrusxqoan0b.x.pipedream.net/",{"user": instance.id,'ip':ip_address},content_type='application/xhtml+xml')
        

post_save.connect(post_save_session_reciver,sender=User)

