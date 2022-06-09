import random, string
from datetime import timedelta
from django.db import models
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils import timezone
from PIL import Image

from unixtimestampfield.fields import UnixTimeStampField
import uuid

from User.models import Organisation

User = get_user_model()

def image_path(instance, filename):
    return 'file/image/{0}/{1}'.format(instance.id, filename)

def image_thumbnail_path(instance, filename):
    return 'file/image/{0}/thumbnail/{1}'.format(instance.id, filename)

def video_path(instance, filename):
    return 'file/video/{0}/{1}'.format(instance.id, filename)

def video_thumbnail_path(instance, filename):
    return 'file/video/{0}/thumbnail/{1}'.format(instance.id, filename)


def set_url():
	url = ''.join(random.choices(string.ascii_lowercase + string.digits, k=250))
	while url in [n.token for n in UniqueURL.objects.all()]:
		url = ''.join(random.choices(string.ascii_lowercase + string.digits, k=250))
	return url

class ImageFiles(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = UnixTimeStampField(auto_now_add=True)
    created_at_numeric = UnixTimeStampField(use_numeric=True, default=timezone.now)
    description = models.CharField(max_length=255, blank=True, null=True)
    file = models.ImageField(upload_to=image_path)
    latitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    longitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    name = models.CharField(max_length=255)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, blank=True, null=True)
    thumbnail = models.ImageField(upload_to=image_thumbnail_path, blank=True, null=True)
    upload_by = models.CharField(max_length=255)
    view_permission = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name
    
    def in_group(self):
        return self.groups.all()
    
    def type(self):
        return "image"

class VideoFiles(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = UnixTimeStampField(auto_now_add=True)
    created_at_numeric = UnixTimeStampField(use_numeric=True, default=timezone.now)
    description = models.CharField(max_length=255, blank=True, null=True)
    file = models.FileField(upload_to=video_path)
    latitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    longitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    name = models.CharField(max_length=255)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, blank=True, null=True)
    thumbnail = models.ImageField(upload_to=video_thumbnail_path, blank=True, null=True)
    upload_by = models.CharField(max_length=255)
    view_permission = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name
    
    def in_group(self):
        return self.groups.all()
    
    def type(self):
        return "video"



class FileGroups(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = UnixTimeStampField(auto_now_add=True)
    created_at_numeric = UnixTimeStampField(use_numeric=True, default=timezone.now)
    created_by = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image_files = models.ManyToManyField(ImageFiles, blank=True, related_name="groups")
    video_files = models.ManyToManyField(VideoFiles, blank=True, related_name="groups")
    name = models.CharField(max_length=100)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, blank=True, null=True)
    view_permission = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name
    
    def type(self):
        return "group"


class UniqueURL(models.Model):
    TYPE = (
        ("image", "image"),
        ("video", "video"),
        ("group", "group")
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=200)
    expired_hrs = models.IntegerField(default=24)
    info = models.CharField(max_length=255, null=True, blank=True)
    obj_id = models.CharField(max_length=250)
    token = models.CharField(max_length=255, default=set_url)
    type = models.CharField(max_length=200, choices=TYPE)
    visited = models.IntegerField(default=0)

    def get_object(self):
        if self.type == "image":
            return get_object_or_404(ImageFiles, id=self.obj_id)
        if self.type == "video":
            return get_object_or_404(VideoFiles, id=self.obj_id)
        if self.type == "group":
            return get_object_or_404(FileGroups, id=self.obj_id)
    
    def is_valid(self):
        if timezone.now() < self.created_at + timedelta(hours=self.expired_hrs):
            return True
        self.delete()
        return False
    


@receiver(models.signals.post_delete, sender=ImageFiles)
def auto_delete_image_on_delete(sender, instance, **kwargs):
    try:
        instance.file.delete(save=False)
    except:
        pass

@receiver(models.signals.pre_save, sender=ImageFiles)
def auto_delete_image_on_change(sender, instance, **kwargs):
    try:
        old_file = ImageFiles.objects.get(id=instance.id).file
        new_file = instance.file
        if not old_file == new_file:
            old_file.delete(save=False)
    except:
        pass

@receiver(models.signals.post_delete, sender=VideoFiles)
def auto_delete_image_on_delete(sender, instance, **kwargs):
    try:
        instance.file.delete(save=False)
    except:
        pass

@receiver(models.signals.pre_save, sender=VideoFiles)
def auto_delete_image_on_change(sender, instance, **kwargs):
    try:
        old_file = VideoFiles.objects.get(id=instance.id).file
        new_file = instance.file
        if not old_file == new_file:
            old_file.delete(save=False)
    except:
        pass

