# Generated by Django 3.1.4 on 2021-11-14 22:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('permission', '0004_role_userrole'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userrole',
            old_name='name',
            new_name='role',
        ),
    ]
