import logging

from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from api.apps.user.utils import ensure_user_associated_with_venue
from api.apps.venue.models import UserData, User

log = logging.getLogger('api')


class UserProfileSerializer(serializers.ModelSerializer):
	mobile = serializers.CharField(allow_blank=True, required=False)
	address1 = serializers.CharField(allow_blank=True, required=False)
	address2 = serializers.CharField(allow_blank=True, required=False)
	city = serializers.CharField(allow_blank=True, required=False)
	country = serializers.CharField(allow_blank=True, required=False)

	class Meta:
		model = UserData
		fields = ('first_name', 'last_name', 'mobile', 'address1', 'address2', 'city', 'country',)

	def update(self, instance, validated_data):
		try:
			if (
				instance.mobile != validated_data.get('mobile', instance.mobile) and
				validated_data.get('mobile_confirmed', False) is not True
			):
				validated_data['mobile_confirmed'] = False

			return super(UserProfileSerializer, self).update(instance, validated_data)
		except KeyError as e:
			raise KeyError(f"Field `{str(e)}` is required")


class UserSerializer(serializers.ModelSerializer):
	mobile = serializers.CharField(source='profile.mobile', allow_blank=True, required=False)
	first_name = serializers.CharField(source='profile.first_name')
	last_name = serializers.CharField(source='profile.last_name')
	address1 = serializers.CharField(source='profile.address1', allow_blank=True, required=False)
	address2 = serializers.CharField(source='profile.address2', allow_blank=True, required=False)
	city = serializers.CharField(source='profile.city', allow_blank=True, required=False)
	country = serializers.CharField(source='profile.country', allow_blank=True, required=False)
	mobile_confirmed = serializers.BooleanField(
		source='profile.mobile_confirmed', default=False, required=False)

	role = serializers.SerializerMethodField()

	class Meta:
		model = User
		extra_kwargs = {'password': {'read_only': True}}
		fields = (
			'email',
			'mobile',
			'role',
			'first_name',
			'last_name',
			'full_name',
			'date_joined',
			'address1',
			'address2',
			'city',
			'country',
			'mobile_confirmed',
			'is_active'
		)

	def get_role(self, instance: User):
		venue = self.context.get('request').get('venue')
		try:
			return instance.roles.filter(venue=venue).first().name
		except AttributeError:
			return None


class ActivateUserSerializer(UserSerializer):
	first_name = serializers.CharField(source='profile.first_name', required=False)
	last_name = serializers.CharField(source='profile.last_name', required=False)

	def update(self, instance, validated_data):
		instance.is_active = True
		instance.save()
		return instance


class EditUserSerializer(UserSerializer):
	def update(self, instance, validated_data):

		profile_data = None
		try:
			profile_data = validated_data.pop('profile')
		except KeyError:
			if not self.partial:
				raise ParseError({'error': "Missing profile information"})

		instance = super(EditUserSerializer, self).update(instance, validated_data)

		if profile_data:
			try:
				profile = instance.profile
			except User.profile.RelatedObjectDoesNotExist:
				profile = UserData()

			instance.profile = profile
			instance.profile.user = instance
			UserProfileSerializer().update(instance.profile, profile_data)

		return instance


class CreateUserSerializer(UserSerializer):
	def create(self, validated_data):
		try:
			# Create the user profile
			profile_data = validated_data.pop('profile', {'mobile': ''})

			with transaction.atomic():
				profile_data['user'] = User.objects.create_user(
					email=validated_data['email'],
					password=validated_data['password'],
					is_active=False
				)
				UserData.objects.create(**profile_data)
				# only do this if user signup for venue, if not venue skip it
				venue = self.context.get("request").venue if self.context.get("request") else None
				if venue:
					ensure_user_associated_with_venue(profile_data['user'], venue)

			return profile_data['user']
		except KeyError as e:
			log.error(e)
			raise ParseError({'error': "Some data is missing"})

	class Meta(UserSerializer.Meta):
		fields = UserSerializer.Meta.fields + ('password',)
		extra_kwargs = {'password': {'write_only': True}}
