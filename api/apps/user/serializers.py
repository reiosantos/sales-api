import logging

from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from api.apps.permission.models import Permission
from api.apps.user.models import DashboardSection, VenueViewerType
from api.apps.user.utils import ensure_user_associated_with_venue
from api.apps.venue.models import Role, UserData, User
from api.apps.venue.serializers import VenueSerializer

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
	venues = VenueSerializer(many=True, read_only=True)
	user_type = serializers.StringRelatedField(source='user_type.name')
	role = serializers.StringRelatedField(source='role.name')

	sections = serializers.SerializerMethodField()
	permissions = serializers.SerializerMethodField()

	class Meta:
		model = User
		extra_kwargs = {'password': {'read_only': True}}
		fields = (
			'email',
			'mobile',
			'user_type',
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
			'sections',
			'permissions',
			'venues',
			'is_active'
		)

	def get_sections(self, instance):
		venue = self.context.get('request').venue
		return DashboardSection.objects.visible_to(instance, venue).values_list(
			'route_name', flat=True)

	def get_permissions(self, instance):
		venue = self.context.get('request').query_params.get('venue')
		return instance.viewer_types.filter(venue__url_component=venue) \
			.values_list('permissions__permission_name', flat=True)


class ActivateUserSerializer(UserSerializer):
	first_name = serializers.CharField(source='profile.first_name', required=False)
	last_name = serializers.CharField(source='profile.last_name', required=False)

	def update(self, instance, validated_data):
		instance.is_active = True
		instance.save()
		return instance


class DashboardSectionSerializer(serializers.ModelSerializer):
	value = serializers.CharField(source='route_name')
	display_name = serializers.CharField(source='name')

	class Meta:
		model = DashboardSection
		fields = ('value', 'display_name')


class VenueViewerTypeSerializer(serializers.ModelSerializer):
	value = serializers.IntegerField(source='pk', read_only=True)
	display_name = serializers.CharField(source='name')

	sections = serializers.SlugRelatedField(
		slug_field='route_name',
		queryset=DashboardSection.objects.all(),
		many=True,
	)

	permissions = serializers.SlugRelatedField(
		slug_field='permission_name',
		queryset=Permission.objects.all(),
		many=True,
		required=False
	)

	class Meta:
		model = VenueViewerType
		fields = (
			'value',
			'display_name',
			'sections',
			'permissions'
		)

	def create(self, validated_data):
		validated_data['venue'] = self.context['request'].venue
		return super(VenueViewerTypeSerializer, self).create(validated_data)


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
					role=Role.objects.get_or_create(name='Role')[0],
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
			raise ParseError({'error': "Some data was missing"})

	class Meta(UserSerializer.Meta):
		fields = UserSerializer.Meta.fields + ('password',)
		extra_kwargs = {'password': {'write_only': True}}
