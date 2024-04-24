from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Request

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password','email']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class TaskSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=100)


class RequestSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    def get_image_url(self, obj):
        if obj.media_file:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.media_file.url)
        return None
    class Meta:
        model = Request
        fields = ['id','request_time','text','status','error','image_url']