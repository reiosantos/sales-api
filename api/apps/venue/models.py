from datetime import datetime
from typing import Union

import pytz
from django.conf import settings
from django.conf.global_settings import LANGUAGES
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django_countries.fields import CountryField
from timezone_field import TimeZoneField

from api.apps.common.fields import LowerCaseCharField
from api.apps.common.model_mixins import BaseModelMixin
from api.apps.common.util import convert_to_python_date_string_format
from api.apps.permission.models import Role


class Venue(BaseModelMixin):
	# Use this with the datetime.strftime method
	TIME_FORMAT = '%I:%M %p'

	name = models.CharField(max_length=100, blank=True, null=True)
	address = models.TextField(blank=True, null=True)
	active = models.BooleanField(default=True, blank=False, null=False)
	url_component = LowerCaseCharField(max_length=200, blank=False, null=False, unique=True)
	users = models.ManyToManyField('User', through='UsersVenues', related_name="venues")
	local_timezone = TimeZoneField(default='Africa/Kampala')
	country = CountryField(default='UG')
	language_code = models.CharField(max_length=7, choices=LANGUAGES, default='en-gb')
	company = models.ForeignKey(
		'company.Company', on_delete=models.CASCADE, null=False, blank=False, related_name='venues')
	logo_url = models.CharField(max_length=200, blank=True, null=True, default='images/logo.png')

	def __str__(self):
		return self.name

	def get_setting_value(self, setting_variable, default=None):
		try:
			return VenueSettingValue.objects.filter(
				setting__var_define=setting_variable, venue=self).get().value
		except VenueSettingValue.DoesNotExist:
			return default

	def set_setting_value(self, setting_variable, value: Union[str, int]):
		"""
		Set a setting on this venue.
		Args:
			setting_variable (string): The name of the setting
			value (Union[str, int])): The value of the variable
		"""
		setting_value, created = self.setting_values.get_or_create(
			setting=VenueSetting.objects.get_or_create(var_define=setting_variable)[0],
			defaults={'value': value}
		)
		if not created and setting_value != value:
			setting_value.value = value
			setting_value.save()

	@property
	def support_email_address(self):
		"""Email address for support requests for the Venue"""
		support_email = self.get_setting_value(
			'DEFAULT_SUPPORT_EMAIL') or settings.DEFAULT_SUPPORT_EMAIL
		return '%s-%s' % (self.url_component, support_email)

	@property
	def dashboard_url(self):
		return settings.DASHBOARD_URL % self.url_component \
			if "%s" in settings.DASHBOARD_URL else settings.DASHBOARD_URL

	@property
	def rest_api_url(self):
		return settings.BASE_URL % self.url_component \
			if "%s" in settings.BASE_URL else settings.BASE_URL

	@property
	def formatted_time(self):
		venue_time = self.get_setting_value('dateFormat.shortTime', 'HH:mm')
		return convert_to_python_date_string_format(venue_time)

	@property
	def formatted_date(self):
		venue_time = self.get_setting_value('dateFormat.mediumDate', 'yyyy-MMM-dd')
		return convert_to_python_date_string_format(venue_time)

	@property
	def formatted_datetime(self):
		venue_time = self.get_setting_value('dateFormat.medium', 'yyyy-MMM-dd HH:mm')
		return convert_to_python_date_string_format(venue_time)

	def get_in_local_time(self, time_to_convert):
		"""
		Converts naive python datetime (without tzinfo) into venue's local time zone.
		Does not touch time, just sets timezone
		:param time_to_convert: datetime.datetime to be converted
		:return: non-naive datetime.datetime with tzinfo set to venue's timezone
		"""
		if not time_to_convert:
			return None
		timezone = pytz.timezone(str(self.local_timezone))
		return timezone.localize(time_to_convert)


class UserManager(BaseUserManager):
	use_in_migrations = True

	def _create_user(self, email, password, is_admin, is_active=True, **extra_fields):
		"""
		Creates and saves a User with the given username, email and password.
		"""

		if not email:
			raise ValueError('The given username/email must be set')

		email = self.normalize_email(email)
		user = self.model(
			email=email, is_active=is_active, is_admin=is_admin, date_joined=datetime.now(),
			**extra_fields)

		user.set_password(password)
		user.save()
		return user

	def create_user(self, email, password=None, **extra_fields):
		return self._create_user(email, password, False, **extra_fields)

	def create_superuser(self, email, password, **extra_fields):
		return self._create_user(email, password, True, **extra_fields)


class User(BaseModelMixin, AbstractBaseUser, PermissionsMixin):
	"""
	API user profile
	"""
	email = models.EmailField(max_length=100, blank=True, null=True, unique=True, db_index=True)
	is_active = models.BooleanField(db_column='active', default=False)
	date_joined = models.DateTimeField(blank=True, null=True, default=datetime.now)
	is_admin = models.BooleanField(default=False, null=True)

	REQUIRED_FIELDS = []
	USERNAME_FIELD = 'email'

	objects = UserManager()

	def is_venue_admin(self, venue: Venue):
		return self.roles.filter(venue=venue, name=Role.ADMIN).exists()

	def is_staff(self, venue: Venue):
		return self.roles.filter(venue=venue, name=Role.STAFF).exists()

	@property
	def is_superuser(self):
		return self.is_admin

	def is_venue_manager(self, venue):
		"""
		Whether or not the user is a 'manager' / 'admin' at a given venue.
		"""
		return self.roles.filter(venue=venue, name=Role.MANAGER).exists()

	def is_venue_user(self, venue):
		"""
		Whether or not the user is a 'manager' / 'admin' at a given venue.
		"""
		return self.roles.filter(venue=venue, name=Role.DEFAULT).exists()

	def get_short_name(self):
		return self.email

	def get_full_name(self):
		return self.full_name

	# Grappelli autocomplete
	@staticmethod
	def autocomplete_search_fields():
		return (
			'profile__first_name__icontains',
			'profile__last_name__icontains',
			'email__icontains',
		)

	def __str__(self):
		return self.email

	@property
	def full_name(self):
		try:
			return '%s %s' % (self.profile.first_name, self.profile.last_name,)
		except UserData.DoesNotExist:
			return ''


class UserData(BaseModelMixin):
	user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
	first_name = models.CharField(max_length=100, blank=True, null=True)
	last_name = models.CharField(max_length=100, blank=True, null=True)
	mobile = models.CharField(max_length=45, blank=True, null=True)
	address1 = models.CharField(max_length=200, blank=True, null=True)
	address2 = models.CharField(max_length=200, blank=True, null=True)
	city = models.CharField(max_length=100, blank=True, null=True)
	country = models.CharField(max_length=100, blank=True, null=True)
	mobile_confirmed = models.BooleanField(default=False)

	def __str__(self):
		return str(self.user)


class UsersVenues(BaseModelMixin):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	venue = models.ForeignKey(Venue, on_delete=models.CASCADE)

	def __str__(self):
		return f'{str(self.venue)} - {str(self.user)}'

	class Meta:
		verbose_name_plural = 'Users Venues'
		unique_together = (('user', 'venue',),)


class VenueSetting(BaseModelMixin):
	label = models.CharField(max_length=200, blank=True, null=True)
	CHOICES_KEY = (
		('dateFormat.shortTime', 'Time format (e.g. HH:mm)'),
		('dateFormat.mediumDate', 'Date format (e.g. dd-MMM-yyy)'),
		('dateFormat.medium', 'Date format with time (e.g. dd-MMM-yyyy HH:mm)'),
		('dateFormat.full', 'Date format with day-of-week and time (e.g. EEE d MMM HH:mm)'),
		('TERMS_URL', 'T&C link'),
		('PRIVACY_POLICY_URL', 'Privacy Policy link'),
		('DEFAULT_LANGUAGE_CODE', 'Default language (example: en-us)'),
		('ENABLE_DEPOSIT', 'Enable usage of the Deposit system for payments'),
		('DEFAULT_CURRENCY', 'Default currency for the Deposit system (example: usd, ush,...)'),
		('MANDATORY_CREDIT_CARD',
		 'User must enter their credit card info before accessing other resources'),
		('STARTING_DAY_IN_WEEK',
		 'Starting day in week for calendar, format: 0=Sunday, 1=Monday, 2=Tuesday, 3=Wednesday,'
		 ' 4=Thursday, 5=Friday, 6=Saturday'),
		('VENUE_ADMIN_EMAIL', 'Venue Admin email'),
		('DEFAULT_SUPPORT_EMAIL', 'Venue Support Email'),
		('ALLOW_SELLING_PRICE_BELOW_BUYING_PRICE', 'Allow selling price to be less than buying price'),
	)

	DICT_OF_CHOICES = {key: value for (key, value) in CHOICES_KEY}

	var_define = models.CharField(max_length=100, choices=CHOICES_KEY, unique=True, null=True)

	def __str__(self):
		return self.DICT_OF_CHOICES.get(self.var_define, self.var_define)


class VenueSettingValue(BaseModelMixin):
	venue = models.ForeignKey(Venue, related_name='setting_values', on_delete=models.CASCADE)
	setting = models.ForeignKey(VenueSetting, on_delete=models.CASCADE)
	value = models.TextField(blank=True, null=True)

	class Meta:
		# Setting must be unique for Venue.
		unique_together = (('venue', 'setting',),)

	def __str__(self):
		return '%s %s: %s' % (str(self.venue), str(self.setting), self.value)
