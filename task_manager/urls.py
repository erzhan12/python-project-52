from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # path('users/', views.users_list, name='users'),  # example view function
    # path('login/', views.login_view, name='login'),
    # path('users/create/', views.register_view, name='register'),
]
