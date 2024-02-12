from django.urls import path

from . import views
from .views import MyTokenObtainPairView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    
    # Authentication and Authorization
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout', views.logout, name='logout'),

    # Todo
    path('create-todo', views.create_todo, name='Create new todo'),
    path('get-todos', views.get_todos, name='Get User todos '),
    

]