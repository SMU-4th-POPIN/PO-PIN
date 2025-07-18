# Generated by Django 5.2.1 on 2025-07-09 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0007_statuspost_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='companionpost',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='companion_posts', to='community.companiontag', verbose_name='태그'),
        ),
        migrations.AlterField(
            model_name='proxypost',
            name='status',
            field=models.CharField(choices=[('모집중', '모집중'), ('긴급모집', '긴급모집'), ('마감', '마감')], max_length=20, verbose_name='모집상태'),
        ),
    ]
