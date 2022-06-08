from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.contrib.auth import get_user_model

from Files.models import FileGroups, ImageFiles, UniqueURL, VideoFiles
from User.models import Organisation

User = get_user_model()

class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    organisation = OrganisationSerializer(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'is_exec', 'organisation', 'created_at']

class ImageFilesSerializers(serializers.ModelSerializer):
    class Meta:
        model = ImageFiles
        fields = ['id', 'created_at', 'description', 'latitude', 'longitude', 'name', 'upload_by', 'url']

class VideoFilesSerializers(serializers.ModelSerializer):
    class Meta:
        model = VideoFiles
        fields = ['id', 'created_at', 'description', 'image', 'latitude', 'longitude', 'name', 'upload_by', 'url']




class FileGroupsSerializers(serializers.ModelSerializer):
    image_files = ImageFilesSerializers(many=True, read_only=True)
    video_files = VideoFilesSerializers(many=True, read_only=True)
    view_permission = UserSerializer(many=True, read_only=True)
    class Meta:
        model = FileGroups
        fields = ['id', 'created_at', 'created_by', 'description', 'image_files', 'video_files', 'name', 'view_permission']


class BossFileGroupSerializers(serializers.ModelSerializer):
    class Meta:
        model = FileGroups
        fields = ['id', 'name', 'description']


class BossImageFilesSerializers(serializers.ModelSerializer):
    view_permission = UserSerializer(many=True, read_only=True)
    in_group = BossFileGroupSerializers(many=True, read_only=True)
    class Meta:
        model = ImageFiles
        fields = ['id', 'created_at', 'description', 'latitude', 'longitude', 'name', 'upload_by', 'url', 'view_permission', 'in_group']

class BossVideoFilesSerializers(serializers.ModelSerializer):
    view_permission = UserSerializer(many=True, read_only=True)
    in_group = FileGroupsSerializers(many=True, read_only=True)
    class Meta:
        model = VideoFiles
        fields = ['id', 'created_at', 'description', 'image', 'latitude', 'longitude', 'name', 'upload_by', 'url', 'view_permission', 'in_group']

class UniqueUrlSerializers(serializers.ModelSerializer):
    class Meta:
        model = UniqueURL
        fields = ['id','created_at', 'created_by', 'expired_hrs', 'info', 'token', "type", 'visited']



def get_object_by_type(obj):
    data = True
    if obj.type == "image":
        file = get_object_or_404(ImageFiles, id=obj.obj_id)
        data = ImageFilesSerializers(file).data
    if obj.type == "video":
        file = get_object_or_404(VideoFiles, id=obj.obj_id)
        data = VideoFilesSerializers(file).data
    if obj.type == "group":
        file = get_object_or_404(FileGroups, id=obj.obj_id)
        data = FileGroupsSerializers(file).data
    return data

    