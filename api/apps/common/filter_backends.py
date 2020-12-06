import coreschema
from django.utils.encoding import force_str
from rest_framework.filters import BaseFilterBackend
import coreapi


class VenueFilterBackend(BaseFilterBackend):
	search_param = 'venue'
	search_title = 'Venue Name'

	def get_schema_fields(self, view):
		assert coreapi is not None, 'coreapi must be installed to use `get_schema_fields()`'
		assert coreschema is not None, 'coreschema must be installed to use `get_schema_fields()`'
		return [
			coreapi.Field(
				name=self.search_param,
				location='query',
				required=False,
				type='string',
				schema=coreschema.String(
					title=force_str(self.search_title)
				)
			),
		]

	def get_schema_operation_parameters(self, view):
		pass

	def filter_queryset(self, request, queryset, view):
		return queryset
