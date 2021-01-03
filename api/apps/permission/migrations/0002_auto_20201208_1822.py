# Generated by Django 3.1.4 on 2020-12-08 18:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
	dependencies = [
		('permission', '0001_initial'),
	]

	operations = [
		migrations.RenameField(
			model_name='permission',
			old_name='created_date',
			new_name='modified_at',
		),
		migrations.RemoveField(
			model_name='permission',
			name='modified_date',
		),
		migrations.AddField(
			model_name='permission',
			name='created_at',
			field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
			preserve_default=False,
		),
	]
