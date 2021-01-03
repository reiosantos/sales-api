# Generated by Django 3.1.4 on 2021-01-03 12:20

from django.db import migrations, models


class Migration(migrations.Migration):
	initial = True

	dependencies = [
	]

	operations = [
		migrations.CreateModel(
			name='Customer',
			fields=[
				('id', models.AutoField(auto_created=True, primary_key=True, serialize=False,
										verbose_name='ID')),
				('created_at', models.DateTimeField(auto_now_add=True, null=True)),
				('modified_at', models.DateTimeField(auto_now=True, null=True)),
				('name', models.CharField(max_length=120)),
				('email', models.EmailField(max_length=254, null=True)),
				('contact', models.CharField(max_length=20, null=True)),
				('address', models.CharField(max_length=200, null=True)),
			],
			options={
				'abstract': False,
			},
		),
	]