# Generated by Django 3.2.14 on 2022-09-11 19:54

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyProperties',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PIN', models.TextField()),
                ('TITLE', models.TextField()),
                ('PROPERTY_DETAILS', models.TextField()),
                ('PROPERTY_PHOTOS', django.contrib.postgres.fields.ArrayField(base_field=models.ImageField(upload_to='property_photos'), size=12)),
            ],
        ),
    ]
