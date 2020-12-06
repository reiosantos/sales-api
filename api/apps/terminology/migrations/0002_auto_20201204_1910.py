# Generated by Django 3.1.4 on 2020-12-04 19:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
	initial = True

	dependencies = [
		('venue', '0001_initial'),
		('terminology', '0001_initial'),
	]

	operations = [
		migrations.AddField(
			model_name='translation',
			name='venue',
			field=models.ForeignKey(blank=True, null=True,
									on_delete=django.db.models.deletion.SET_NULL, to='venue.venue'),
		),
		migrations.AlterUniqueTogether(
			name='translation',
			unique_together={('venue', 'term', 'language')},
		),
	]
