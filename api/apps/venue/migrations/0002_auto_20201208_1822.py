# Generated by Django 3.1.4 on 2020-12-08 18:22

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
	dependencies = [
		('venue', '0001_initial'),
	]

	operations = [
		migrations.RenameField(
			model_name='role',
			old_name='created_date',
			new_name='modified_at',
		),
		migrations.RenameField(
			model_name='user',
			old_name='created_date',
			new_name='modified_at',
		),
		migrations.RenameField(
			model_name='userdata',
			old_name='created_date',
			new_name='modified_at',
		),
		migrations.RenameField(
			model_name='usersvenues',
			old_name='created_date',
			new_name='modified_at',
		),
		migrations.RenameField(
			model_name='usertype',
			old_name='created_date',
			new_name='modified_at',
		),
		migrations.RenameField(
			model_name='venue',
			old_name='created_date',
			new_name='modified_at',
		),
		migrations.RenameField(
			model_name='venuesetting',
			old_name='created_date',
			new_name='modified_at',
		),
		migrations.RenameField(
			model_name='venuesettingvalue',
			old_name='created_date',
			new_name='modified_at',
		),
		migrations.RemoveField(
			model_name='role',
			name='modified_date',
		),
		migrations.RemoveField(
			model_name='user',
			name='modified_date',
		),
		migrations.RemoveField(
			model_name='userdata',
			name='modified_date',
		),
		migrations.RemoveField(
			model_name='usersvenues',
			name='modified_date',
		),
		migrations.RemoveField(
			model_name='usertype',
			name='modified_date',
		),
		migrations.RemoveField(
			model_name='venue',
			name='logo',
		),
		migrations.RemoveField(
			model_name='venue',
			name='modified_date',
		),
		migrations.RemoveField(
			model_name='venuesetting',
			name='modified_date',
		),
		migrations.RemoveField(
			model_name='venuesettingvalue',
			name='modified_date',
		),
		migrations.AddField(
			model_name='role',
			name='created_at',
			field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
			preserve_default=False,
		),
		migrations.AddField(
			model_name='user',
			name='created_at',
			field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
			preserve_default=False,
		),
		migrations.AddField(
			model_name='userdata',
			name='created_at',
			field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
			preserve_default=False,
		),
		migrations.AddField(
			model_name='usersvenues',
			name='created_at',
			field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
			preserve_default=False,
		),
		migrations.AddField(
			model_name='usertype',
			name='created_at',
			field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
			preserve_default=False,
		),
		migrations.AddField(
			model_name='venue',
			name='created_at',
			field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
			preserve_default=False,
		),
		migrations.AddField(
			model_name='venue',
			name='logo_url',
			field=models.CharField(blank=True, default='images/logo.png', max_length=200,
								   null=True),
		),
		migrations.AddField(
			model_name='venuesetting',
			name='created_at',
			field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
			preserve_default=False,
		),
		migrations.AddField(
			model_name='venuesettingvalue',
			name='created_at',
			field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
			preserve_default=False,
		),
		migrations.AlterField(
			model_name='user',
			name='role',
			field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
									related_name='users', to='venue.role'),
		),
	]