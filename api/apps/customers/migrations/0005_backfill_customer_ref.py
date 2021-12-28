# Generated by Django 3.1.4 on 2021-12-28 12:47

from django.db import migrations


def fill_Refs(apps, schema_editor, reverse=False):
	Customer = apps.get_model('customers', 'Customer')

	if reverse:
		for cus in Customer.objects.iterator():
			cus.ref = None
			cus.save()
		return

	for cus in Customer.objects.iterator():
		cus.ref = "{}{}{}".format("CUS", cus.created_at.month, format(cus.pk, '06d'))
		cus.save()


def revert_fill_refs(apps, schema_editor):
	fill_Refs(apps, schema_editor, reverse=True)


class Migration(migrations.Migration):
	dependencies = [
		('customers', '0004_customer_ref'),
	]
	operations = [
		migrations.RunPython(fill_Refs, revert_fill_refs)
	]
