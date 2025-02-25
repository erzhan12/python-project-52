from django.urls import path
from .views import (
    UserListView, UserUpdateView,
    UserDeleteView, UserCreateView,
    UserLoginView, UserLogoutView
)

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('users/', UserListView.as_view(), name='users'),
    path('users/<int:pk>/update/',
         UserUpdateView.as_view(), name='user_update'),
    path('users/<int:pk>/delete/',
         UserDeleteView.as_view(), name='user_delete'),
    path('users/create/', UserCreateView.as_view(), name='user_create'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]
