# Generated by Django 2.0 on 2018-02-11 18:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('github', '0005_organization'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='user',
        ),
    ]