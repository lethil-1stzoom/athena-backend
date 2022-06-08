from django.db import models
import uuid
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from unixtimestampfield.fields import UnixTimeStampField


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

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []
	
	objects = CustomUserManager()
	
	def __str__(self):
		return self.email
	
	def name(self):
		return self.first_name


