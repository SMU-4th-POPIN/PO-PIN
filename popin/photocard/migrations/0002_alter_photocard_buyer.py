# Generated by Django 5.2.1 on 2025-06-24 04:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photocard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photocard',
            name='buyer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='buy', to='photocard.tempuser'),
        ),
    ]
