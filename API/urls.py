from django.urls import path, include
from .views import *


urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    path('login/', login),
    path('validate/', validate),
    path('image/', image_api),
    path('video/', video_api),
    path('group/', group_api),
    path('image/<uuid:id>/', image_edit),
    path('video/<uuid:id>/', video_edit),
    path('group/<uuid:id>/', group_edit),
    path('users/', users),
    path('users/<uuid:id>', users_edit),
    path('edit/user/', edit_info),
    path('share/', share),
    path('share/<uuid:id>/', share_edit),
    path('temp/file/<str:token>/', get_from_share),
    ]