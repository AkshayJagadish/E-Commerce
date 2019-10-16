# Generated by Django 2.2.1 on 2019-06-26 15:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0005_remove_client_key'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReqInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('home_phone', models.CharField(max_length=15)),
                ('my_pp', models.FileField(blank=True, null=True, upload_to='profile_picture/')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
