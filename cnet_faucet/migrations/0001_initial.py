# Generated by Django 5.0.6 on 2024-07-05 11:29

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FaucetRequest',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('wallet_address', models.CharField(max_length=64)),
                ('request_time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
