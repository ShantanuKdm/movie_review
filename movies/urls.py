from django.urls import path
from .views import RegistserView,LoginView

urlpatterns = [
    path('register',RegistserView.as_view(), name='register'),
    path('login',LoginView.as_view(), name='login')
]