from .views import RegisterAPI
from django.urls import path
# from knox import views as knox_views
# from knox import views as knox_views
from .views import LoginAPI
from django.urls import path,include

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/',LoginAPI.as_view(), name='login'),
]