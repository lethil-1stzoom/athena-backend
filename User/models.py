from django.db import models
import uuid
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification

from User.emails import send_email


class CustomUserManager(BaseUserManager):
	def create_user(self, email, password, **extra_fields):
		if not email:
			raise ValueError(_('The Email must be set'))
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save()
		return user

	def create_superuser(self, email, password, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		extra_fields.setdefault('is_active', True)


		if extra_fields.get('is_staff') is not True:
			raise ValueError(_('Superuser must have is_staff=True.'))
		if extra_fields.get('is_superuser') is not True:
			raise ValueError(_('Superuser must have is_superuser=True.'))
		return self.create_user(email, password, **extra_fields)

	def create_staff(self, email, password, **extra_fields):
		extra_fields.setdefault('is_staff', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError(_('Staff must have is_staff=True.'))
		return self.create_user(email, password, **extra_fields)



class Organisation(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=200)

	def __str__(self):
		return self.name

class CustomUser(AbstractUser):
	username = None
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	created_at = models.DateTimeField(auto_now_add=True)
	email = models.EmailField(_('email address'), unique=True)
	is_exec = models.BooleanField(default=False)
	organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, blank=True, null=True, related_name="users")
	fcmDevice = models.ManyToManyField(FCMDevice, blank=True)
	notify = models.BooleanField(default=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []
	
	objects = CustomUserManager()
	
	def __str__(self):
		return self.email
	
	def name(self):
		return self.first_name
	
	def edit_fcmDevice(self, token):
		if not self.fcmDevice.filter(registration_id=token).exists():
			fcmDevice = FCMDevice.objects.create(
				registration_id=token,
				type='android'
				)
			fcmDevice.save()
			self.fcmDevice.add(fcmDevice)
			self.save()
	
	def fcmRemove(self, token):
		if self.fcmDevice.filter(registration_id=token).exists():
			token = self.fcmDevice.get(registration_id=token)
			token.delete()
			
	def send_notification(self, title, body, data = {}):
		for fcm in self.fcmDevice.all():
			fcm.send_message(Message(notification=Notification(title=title, body=body), data=data))
	
	def send_notification_email(self, by, subject):
		if self.notify == True and self.is_exec == True:
			email = self.email
			name = self.first_name
			return send_email(email, name, subject, by)
		else:
			pass
	def send_welcome_email(self, by, subject, psw):
		email = self.email
		name = self.first_name
		return send_email(email, name, subject, by, psw)


