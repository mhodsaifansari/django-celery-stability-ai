from django.shortcuts import render
# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer
from .serializers import UserSerializer, LoginSerializer, TaskSerializer, RequestSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from .tasks import generate_image
from .models import Request

class HealthRoute(APIView):
    def get(self, request):
        print(request.user)
        return Response(data={"status":"running"},status=status.HTTP_200_OK)
    
class Register(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        new_user = UserSerializer(data=request.data)
        if new_user.is_valid():
            user=new_user.save()
            refresh = RefreshToken.for_user(user)
            return Response({"status":"success",
                             "tokens":{"refresh_token":str(refresh),
                                    "access_token":str(refresh.access_token)}
                            },status=status.HTTP_201_CREATED)
        return Response({"status":"error","msg":new_user.errors},status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):
    permission_classes = [AllowAny]
    def post(self, request):

        user = LoginSerializer(data=request.data)
        if user.is_valid():
            print(user.validated_data)
            u=User.objects.filter(username=user.validated_data['username'])
            if u.exists():
                u = u.first()
                refresh = RefreshToken.for_user(u)
                return Response({"status":"success","username":u.username,"tokens":{"refresh_token":str(refresh),"access_token":str(refresh.access_token)}},status=status.HTTP_200_OK)
            return Response({"status":"error","msg":"user doesnot exists"},status=status.HTTP_404_NOT_FOUND)
        return Response({"status":"error","msg":user.errors},status=status.HTTP_400_BAD_REQUEST)


class Task(APIView):
    def post(self, request):
        data = TaskSerializer(data=request.data)
        if data.is_valid():
            user=request.user
            r=Request.objects.create(text=data.validated_data['text'],user=user,status=Request.STATUS_CHOICES.PENDING)
            generate_image.apply_async([r.id],countdown=10)

            return Response({"status":"success"},status=status.HTTP_200_OK)
        return Response({"status":"error","msg":data.errors},status=status.HTTP_400_BAD_REQUEST)
        

class TaskList(APIView):
    def get(self,request):
        user=request.user
        r=Request.objects.filter(user=user)
        request_data=RequestSerializer(r,many=True,context={'request': request})
        return Response(request_data.data,status=status.HTTP_200_OK)