import json
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import permissions, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from API.decorators import is_exec

from Files.models import VideoFiles

from .seralizers import *

@api_view(['POST'])
@authentication_classes([])
@permission_classes((permissions.AllowAny, ))
def login(request):
    if request.method == 'POST':
        if isinstance(request.data, str):
            data = json.loads(request.data)
        else:
            data = request.data
        email = data.get('email', '')
        password = data.get('password', '')
        user = authenticate(email=email, password=password)
        if user is not None and not user.is_staff:
            token, created = Token.objects.get_or_create(user=user)
            user = UserSerializer(user).data
            user['token'] = token.key
            response = Response({"user": user})
            response.set_cookie(key='token', value=token.key)
            return response
        return Response({"message": "Something went wrong"}, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def validate(request):
    user = request.user
    if request.method == 'GET':
        data = UserSerializer(user).data
        data['validated'] = True
        return Response(data)

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def image_api(request):
    user = request.user
    organisation = user.organisation
    if request.method == 'GET':
        if user.is_exec:
            image = organisation.imagefiles_set.all()
            data = BossImageFilesSerializers(image, many=True).data
        else:
            image = user.imagefiles_set.all()
            data = ImageFilesSerializers(image, many=True).data
        return Response(data)
    if request.method == 'POST':
        if isinstance(request.data, str):
            data = json.loads(request.data)
        else:
            data = request.data
        name = data.get('name', '')
        description = data.get('description', '')
        file = data.get('file', '')
        latitude = data.get('latitude', '')
        longitude = data.get('longitude', '')
        group_id = data.get('group', '')
        if name != '' and file != '':
            image = ImageFiles.objects.create(
                name=name,
                file=file,
                upload_by=user.email,
                organisation=organisation,
            )
            if description != '':
                image.description = description
            if latitude != '' and longitude != '':
                image.latitude = latitude
                image.longitude = longitude
            image.save()
            if group_id != '':
                group = get_object_or_404(FileGroups, id=group_id)
                group.image_files.add(image)
                group.save()
            if not user.is_exec:
                image.view_permission.add(user)
                data = ImageFilesSerializers(image).data
            else:
                data = BossImageFilesSerializers(image).data
            return Response(data)
        return Response({"message": "Something went wrong"}, status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def video_api(request):
    user = request.user
    organisation = user.organisation
    if request.method == 'GET':
        if user.is_exec:
            video = organisation.videofiles_set.all()
            data = BossVideoFilesSerializers(video, many=True).data
        else:
            video = user.videofiles_set.all()
            data = VideoFilesSerializers(video, many=True).data
        return Response(data)
    if request.method == 'POST':
        if isinstance(request.data, str):
            data = json.loads(request.data)
        else:
            data = request.data
        name = data.get('name', '')
        description = data.get('description', '')
        file = data.get('file', '')
        latitude = data.get('latitude', '')
        longitude = data.get('longitude', '')
        group_id = data.get('group', '')
        if name != '' and file != '':
            video = VideoFiles.objects.create(
                name=name,
                file=file,
                upload_by=user.email,
                organisation=organisation,
            )
            if description != '':
                video.description = description
            if latitude != '' and longitude != '':
                video.latitude = latitude
                video.longitude = longitude
            video.save()
            if group_id != '':
                group = get_object_or_404(FileGroups, id=group_id)
                group.video_files.add(video)
                group.save()
            if not user.is_exec:
                video.view_permission.add(user)
                data = VideoFilesSerializers(video).data
            else:
                data = BossVideoFilesSerializers(video).data
            return Response(data)
        return Response({"message": "Something went wrong"}, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def group_api(request):
    user = request.user
    organisation = user.organisation
    if request.method == 'GET':
        if user.is_exec:
            group = organisation.filegroups_set.all()
        else:
            group = user.filegroups_set.all()
        data = FileGroupsSerializers(group, many=True).data
        return Response(data)
    
    if request.method == 'POST':
        if user.is_exec:
            if isinstance(request.data, str):
                data = json.loads(request.data)
            else:
                data = request.data
            description = data.get('description', '')
            name = data.get('name', '')
            images = data.get('image_files', '')
            videos = data.get('video_files', '')
            view_permission = data.get('view_permission', '')
            if name != '' and description != '':
                group = FileGroups.objects.create(
                    name=name,
                    description=description,
                    created_by=user.email,
                    organisation=organisation,
                )
                if images != '':
                    for id in images:
                        img = get_object_or_404(ImageFiles, id=id)
                        group.image_files.add(img)
                if videos != '':
                    for id in videos:
                        vid = get_object_or_404(VideoFiles, id=id)
                        group.video_files.add(vid)
                if view_permission != '':
                    for id in view_permission:
                        usr = get_object_or_404(User, id=id)
                        if not usr.is_exec:
                            group.view_permission.add(usr)
                group.save()
                data = FileGroupsSerializers(group).data
                return Response(data)
            else:
                Response({"message": "Something went wrong"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response({"status": "Not Authorized"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['PATCH', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@is_exec
def image_edit(request, id):
    image = get_object_or_404(ImageFiles, id=id)
    if request.method == 'PATCH':
        if isinstance(request.data, str):
            data = json.loads(request.data)
        else:
            data = request.data
        description = data.get('description', '')
        name = data.get('name', '')
        view_permission = data.get('view_permission', '')
        if description != '':
            image.description = description
        if name != '':
            image.name = name
        if view_permission != '':
            for id in view_permission:
                usr = get_object_or_404(User, id=id)
                image.view_permission.add(usr)
        image.save()
        data = BossImageFilesSerializers(image).data
        return Response(data)
    if request.method == 'DELETE':
        image.delete()
        return Response({"message": "Deleted Successfully"})

@api_view(['PATCH', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@is_exec
def video_edit(request, id):
    video = get_object_or_404(VideoFiles, id=id)
    if request.method == 'PATCH':
        if isinstance(request.data, str):
            data = json.loads(request.data)
        else:
            data = request.data
        description = data.get('description', '')
        name = data.get('name', '')
        view_permission = data.get('view_permission', '')
        if description != '':
            video.description = description
        if name != '':
            video.name = name
        if view_permission != '':
            for id in view_permission:
                usr = get_object_or_404(User, id=id)
                video.view_permission.add(usr)
        video.save()
        data = BossVideoFilesSerializers(video).data
        return Response(data)
    if request.method == 'DELETE':
        video.delete()
        return Response({"message": "Deleted Successfully"})

@api_view(['PATCH', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@is_exec
def group_edit(request, id):
    group = get_object_or_404(FileGroups, id=id)
    if request.method == 'PATCH':
        if isinstance(request.data, str):
            data = json.loads(request.data)
        else:
            data = request.data
        description = data.get('description', '')
        name = data.get('name', '')
        images = data.get('image_files', '')
        videos = data.get('video_files', '')
        view_permission = data.get('view_permission', '')
        if description != '':
            group.description = description
        if name != '':
            group.name = name
        if images != '':
            for id in images:
                img = get_object_or_404(ImageFiles, id=id)
                group.image_files.add(img)
        if videos != '':
            for id in videos:
                vid = get_object_or_404(VideoFiles, id=id)
                group.video_files.add(vid)
        if view_permission != '':
            for id in view_permission:
                usr = get_object_or_404(User, id=id)
                group.view_permission.add(usr)
        group.save()
        data = FileGroupsSerializers(group).data
        return Response(data)
    if request.method == 'DELETE':
        group.delete()
        return Response({"message": "Deleted Successfully"})


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@is_exec
def users(request):
    user = request.user
    organisation = user.organisation
    if request.method == 'GET':
        usr = organisation.users.exclude(email=user.email)
        data = UserSerializer(usr, many=True).data
        return Response(data)
    
    if request.method == 'POST':
        if isinstance(request.data, str):
            data = json.loads(request.data)
        else:
            data = request.data
        email = data.get('email', '')
        password1 = data.get('password1', '')
        password2 = data.get('password2', '')
        first_name = data.get('name', '')
        is_exec = data.get('is_exec', '')
        if email != '' and first_name != '' and is_exc != '':
            if password1 == password2 and password1 != '':
                user = User.objects.create(
                    email=email,
                    first_name=first_name,
                    is_exec=is_exec
                )
                user.set_password(password1)
                user.save()
                data = UserSerializer(user).data
                return Response(data)
        return Response({"message": "Something went wrong"}, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@is_exec
def users_edit(request, id):
    user = get_object_or_404(User, id=id)

    if request.method == 'DELETE':
        user.delete()
        return Response({"message": "Deleted Successfully"})

@api_view(['DELETE', 'PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_info(request):
    if request.method == 'PATCH':
        if isinstance(request.data, str):
            data = json.loads(request.data)
        else:
            data = request.data
        password1 = data.get('password1', '')
        password2 = data.get('password2', '')
        password = data.get('password', '')
        email = data.get('email', '')
        first_name = data.get('name', '')
        is_exc = data.get('is_exc', '')

        user = authenticate(email=email, password=password)
        if user is not None:
            if password1 != '' and password1 == password2:
                user.set_password(password1)
            if first_name != '':
                user.first_name = first_name
            if is_exc != '':
                user.is_exc = is_exc
            user.save()

    if request.method == 'DELETE':
        user.delete()
        return Response({"message": "Delete Successfully"})


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@is_exec
def share(request):
    user = request.user
    if request.method == 'GET':
        url = []
        l = UniqueURL.objects.all()
        for u in l:
            if u.is_valid():
                url.append(u)
        data = UniqueUrlSerializers(url, many=True).data
        for d in data:
            temp = get_object_or_404(UniqueURL, token=d['token'])
            d["file"] = get_object_by_type(temp)
        return Response(data)
    
    if request.method == 'POST':
        if isinstance(request.data, str):
            data = json.loads(request.data)
        else:
            data = request.data
        expired_hrs = data.get("expired_hrs", "")
        info = data.get("info", "")
        obj_id = data.get("obj_id", "")
        type = data.get("type", "")
        if info != "" and obj_id != "" and type != "":
            url = UniqueURL.objects.create(
                info=info,
                obj_id=obj_id,
                type=type,
                created_by=user.email
            )
            if expired_hrs != "":
                url.expired_hrs = int(expired_hrs)
            url.save()
            data = UniqueUrlSerializers(url).data
            return Response(data)

@api_view(['DELETE', 'PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@is_exec
def share_edit(request, id):
    url = get_object_or_404(UniqueURL, id=id)
    if request.method == 'PATCH':
        if isinstance(request.data, str):
            data = json.loads(request.data)
        else:
            data = request.data
        expired_hrs = data.get("expired_hrs", "")
        info = data.get("info", "")
        if expired_hrs != '':
            url.expired_hrs = expired_hrs
        if info != '':
            url.info = info
        url.save()
        data = UniqueUrlSerializers(data).data
        return Response(data)
    if request.method == 'DELETE':
        url.delete()
        return Response({"message": "Deleted Successfully"})

@api_view(['GET'])
@authentication_classes([])
@permission_classes((permissions.AllowAny, ))
def get_from_share(requesr, token):
    url = get_object_or_404(UniqueURL, token=token)
    if url.is_valid():
        data = get_object_by_type(url)
        url.visited += 1
        url.save()
        return Response(data)
    return Response({"message": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
            
