# Generated by Django 4.2 on 2025-02-24 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ramazan', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='time_period',
            name='date_hejri',
            field=models.CharField(default='null', max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='time_period',
            name='date_shamsi',
            field=models.CharField(default='null', max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='time_period',
            name='image',
            field=models.ImageField(default='null', null=True, upload_to='ramazan_peried/'),
        ),
    ]
