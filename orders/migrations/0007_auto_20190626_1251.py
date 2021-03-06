# Generated by Django 2.2.1 on 2019-06-26 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('account', '0002_email_max_length'),
        ('socialaccount', '0003_extra_data_default_dict'),
        ('orders', '0006_reqinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='reqinfo',
            name='city',
            field=models.CharField(default='Windsor', max_length=20),
        ),
        migrations.AddField(
            model_name='reqinfo',
            name='interested_in',
            field=models.ManyToManyField(to='orders.Category'),
        ),
        migrations.AddField(
            model_name='reqinfo',
            name='province',
            field=models.CharField(choices=[('AB', 'Alberta'), ('MB', 'Manitoba'), ('ON', 'Ontario'), ('QC', 'Quebec')], default='ON', max_length=2),
        ),
        migrations.AddField(
            model_name='reqinfo',
            name='shipping_address',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.DeleteModel(
            name='Client',
        ),
    ]
