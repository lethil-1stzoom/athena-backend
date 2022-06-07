from rest_framework import serializers
from django.contrib.auth import get_user_model

from Files.models import FileGroups, ImageFiles, VideoFiles
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
        fields = ['id', 'email', 'first_name', 'last_name', 'is_exec', 'organisation']

class ImageFilesSerializers(serializers.ModelSerializer):
    class Meta:
        model = ImageFiles
        fields = ['id', 'created_at', 'description', 'latitude', 'longitude', 'name', 'upload_by', 'url']

class VideoFilesSerializers(serializers.ModelSerializer):
    class Meta:
        model = VideoFiles
        fields = ['id', 'created_at', 'description', 'latitude', 'longitude', 'name', 'upload_by', 'url']



class BossImageFilesSerializers(serializers.ModelSerializer):
    view_permission = UserSerializer(many=True, read_only=True)
    class Meta:
        model = ImageFiles
        fields = ['id', 'created_at', 'description', 'latitude', 'longitude', 'name', 'upload_by', 'url', 'view_permission']

class BossVideoFilesSerializers(serializers.ModelSerializer):
    view_permission = UserSerializer(many=True, read_only=True)
    class Meta:
        model = VideoFiles
        fields = ['id', 'created_at', 'description', 'latitude', 'longitude', 'name', 'upload_by', 'url', 'view_permission']



class FileGroupsSerializers(serializers.ModelSerializer):
    image_files = ImageFilesSerializers(many=True, read_only=True)
    video_files = VideoFilesSerializers(many=True, read_only=True)
    view_permission = UserSerializer(many=True, read_only=True)
    class Meta:
        model = FileGroups
        fields = ['id', 'created_at', 'created_by', 'description', 'image_files', 'video_files', 'name', 'view_permission']