from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import * 

from datetime import datetime
from django.http import HttpResponse
# Create your views here.


def index(request):
    now = datetime.now()
    html = f'''
    <html>
        <body>
            <h1>Hello from VK Traders!</h1>
            <p>The current time is { now }.</p>
        </body>
    </html>
    '''
    return HttpResponse(html)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email 
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['is_superuser'] = user.is_superuser

        return token
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
def logout(request):
    # Assuming you are using the simplejwt refresh token approach
    refresh_token = request.GET.get('refresh-token')

    if refresh_token:
        try:
            RefreshToken(refresh_token).blacklist()
            return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)
        except TokenError:
            return Response({"message": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({"message": "Refresh token not provided."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def create_todo(request):
    username = request.GET.get('username')
    todo_data = request.GET.get('todo-data')

    try:
        user_instance = AuthUser.objects.get(username=username)

        todo = Todos.objects.create(
            todo_name=todo_data,
            description='',
            created_by=user_instance 
        )

        return_response={}

        if todo.id:
            return_response['id'] = todo.id
            return_response['message'] = 'New Todo added'

        return Response(return_response, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_todos(request):
    username = request.GET.get('username')

    try: 
        user_instance = AuthUser.objects.get(username=username)

        get_todos = Todos.objects.filter(created_by=user_instance).values().order_by('-created_at')

        return Response(get_todos, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    