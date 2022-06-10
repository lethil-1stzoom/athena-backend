from django.urls import path
from .views import *


urlpatterns = [
    path('temp/file/<str:token>/', get_from_share),
]