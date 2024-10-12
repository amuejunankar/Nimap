# Generated by Django 5.0.6 on 2024-10-09 14:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usrClient', '0004_alter_client_created_by'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='project',
            name='updated_at',
        ),
        migrations.AlterField(
            model_name='project',
            name='users',
            field=models.ManyToManyField(related_name='projects', to=settings.AUTH_USER_MODEL),
        ),
    ]
