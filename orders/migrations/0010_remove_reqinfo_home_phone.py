# Generated by Django 2.2.1 on 2019-06-26 18:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_auto_20190626_1316'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reqinfo',
            name='home_phone',
        ),
    ]
