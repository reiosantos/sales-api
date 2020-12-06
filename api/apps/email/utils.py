import logging

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail.message import EmailMessage
from django.template import TemplateDoesNotExist
from django.template.loader import get_template

# the email address which failed email notifications are sent to
from api.apps.venue.models import Venue

log = logging.getLogger('api')


class EmailAddress:
	def __init__(self, address, name=None):
		self.address = address
		self.name = name

	def address_with_name(self):
		"""
		Name <address>
		:return:
		"""
		if self.name:
			return '%s <%s>' % (self.name, self.address)
		return self.address


class TemplateMixin:
	default_template_name: str = ''

	def __init__(self):
		self.context = None

	@property
	def template_name(self):
		template_name = self.default_template_name
		try:
			template_name = '%s/%s' % (
				self.context.get('request').venue.url_component,
				template_name
			)
			get_template('email/%s.html' % template_name)
			return template_name
		except TemplateDoesNotExist:
			pass
		return self.default_template_name


class CustomEmailMessage(EmailMessage):
	"""
	Templated email message.
	"""
	content_subtype = 'html'
	venue: Venue = None

	def __init__(self, context=None):
		if context:
			request = context.get('request')
			if request and request.venue:
				self.venue = request.venue

		to = list(map(lambda r: r.address_with_name(), self._addressees()))
		try:
			reply_to = self.get_reply_addresses()
		except Exception as e:
			log.error(e)
			reply_to = None

		super(CustomEmailMessage, self).__init__(
			subject=self.get_subject(),
			to=to,
			reply_to=reply_to,
			cc=self.get_cc_list(),
			bcc=self.get_bcc_list(),
			body=self.get_body()
		)

	@property
	def template_name(self):
		"""
		Name of the template.
		"""
		raise NotImplementedError('template_name must be defined')

	def get_body(self):
		"""
		Name of the template.
		"""
		raise NotImplementedError('get_body must be implemented')

	def get_subject(self):
		"""
		Name of the template.
		"""
		raise NotImplementedError('get_subject must be implemented')

	def get_addressees(self):
		raise NotImplementedError('The recipient(s) must be defined')

	@property
	def addressees(self):
		"""
		The recipients.
		"""
		return self.get_addressees()

	def get_bcc_list(self):
		"""
		Implement this to return a list of addresses to BCC
		Returns a list of emails to BCC
		:return: []
		"""
		return []

	def get_cc_list(self):
		"""
		Implement this to return a list of addresses to CC
		Returns a list of emails to CC
		:return: []
		"""
		return []

	def get_reply_addresses(self):
		return [self.get_reply_address()]

	def get_reply_address(self):
		if self.venue:
			return self.venue.support_email_address
		return settings.DEFAULT_SUPPORT_EMAIL

	def _addressees(self):
		"""
		Checks if user has in-app notification configuration and removes them from recipients
		if they chose not to receive the email based on the access_point, resource or action
		"""
		addressees = self.addressees
		if not addressees:
			return []

		addresses = list(filter(lambda x: x is not None and x.address is not None, addressees))

		self.failures = list(filter(lambda x: x is None or x.address is None, addressees))

		# deduplicate the list
		seen = set()
		unique = []
		for a in addresses:
			if a.address not in seen:
				unique.append(a)
				seen.add(a.address)
		addresses = unique
		self.successes = addresses
		return addresses

	def send_failures(self):
		if len(self.failures) > 0:
			failure_email = FailureEmail(self)
			failure_email.send()

	def send(self, fail_silently=False):
		"""Sends the email message."""
		self.send_failures()
		if not self.recipients():
			# Don't bother creating the network connection if there's nobody to
			# send to.
			return 0
		return self.get_connection(fail_silently).send_messages([self])


class ContextEmailMessage(CustomEmailMessage):
	"""
	Templated email.
	"""

	def __init__(self, model_instance, context=None):
		self.instance = model_instance
		self.context = context
		super(ContextEmailMessage, self).__init__(context=self.context)

	def get_body(self):
		request = self.context['request']
		self.context['browser_name'] = request.META.get('HTTP_USER_AGENT', 'Unknown')
		return get_template('email/%s.html' % self.template_name).render(context={
			'instance': self.instance,
			'context': self.context
		})


class WelcomeEmail(ContextEmailMessage):
	"""
	An email which is sent when a user signs up
	"""
	# placeholder until users are associated with different industries
	template_name = 'welcome-user'

	def get_subject(self):
		return 'Welcome to {}'.format(settings.APP_NAME)

	def get_addressees(self):
		return [EmailAddress(self.instance.email, self.instance.full_name)]


class PasswordResetEmail(ContextEmailMessage):
	"""
	An email which is sent when a user asks for password reset
	"""
	template_name = 'password-reset'

	def get_subject(self):
		return 'Password Reset for {}'.format(settings.APP_NAME)

	def get_addressees(self):
		return [EmailAddress(self.instance.email, self.instance.full_name)]


class VerifyUserEmail(ContextEmailMessage):
	"""
	An email which is sent when a usercreate a new account
	"""
	template_name = 'email-verification'

	def get_subject(self):
		return 'Email Verification for {}'.format(settings.APP_NAME)

	def get_addressees(self):
		return [EmailAddress(self.instance.email, self.instance.full_name)]


class FailureEmail(EmailMessage):
	"""
	an email to be sent to VC admin whenever an email is generated to an addressee who doesn't
	have an email address
	"""

	def __init__(self, original_email):
		# the email to send failed email notifications to
		if hasattr(original_email, 'venue') and isinstance(original_email.venue, Venue):
			to = (original_email.venue.get_setting_value(
				'VENUE_ADMIN_EMAIL') or settings.VENUE_ADMIN_EMAIL,)
		else:
			to = (settings.VENUE_ADMIN_EMAIL,)
		# the original email instance from which we get contextual info
		self.original_email = original_email
		# recipient roles which were meant to receive the email but for whom no
		# email address was found
		self.failures = ", ".join(
			list(filter(None, [f.name for f in self.original_email.failures])))
		# the class of the original email, from which we get the event which
		# triggered it
		self.original_email_class = type(original_email).__name__
		# successful recipients of the original email
		self.successes = ", ".join([s.address_with_name() for s in self.original_email.successes])
		body = self.get_body()
		subject = "Failed email"
		super(FailureEmail, self).__init__(subject=subject, body=body, to=to)

	def get_trigger(self):
		string_email_status_dict = {
			'WelcomeEmail': 'User joined',
			'VerifyUserEmail': 'User Verification',
			'PasswordResetEmail': 'Password Reset',
		}

		trigger = string_email_status_dict.get(self.original_email_class, None)
		return trigger

	def get_body(self):
		# construct a plain text body for the email
		full_text = list()
		full_text.append("Dear admin,")
		full_text.append(
			"An email was successfully sent to the following recipient(s): " + self.successes
		)
		full_text.append(
			"The email was also meant to be sent to the following users associated with the event: " +
			self.failures +
			", but their details were not available."
		)
		full_text.append("The email was triggered by the following event: " + self.get_trigger())

		return "\n".join(full_text)


def site_url(request, uri):
	"""
	Append the current site protocol and url to the given uri.
	"""
	site = get_current_site(request)
	if site is not None:
		return '{0}://{1}{2}{3}'.format(
			'https' if settings.SSL_ENABLED else 'http',
			site.name,
			'' if uri.startswith('/') else '/',
			uri
		)
	else:
		# @TODO? handle `site is None`
		pass
