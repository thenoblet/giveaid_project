# Generated by Django 4.2.13 on 2024-07-12 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('giveaid', '0003_alter_user_city_alter_user_country_alter_user_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='unregistereddonation',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='unregistereddonation',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending', max_length=10),
        ),
    ]
