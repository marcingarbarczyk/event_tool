# Generated by Django 4.2.4 on 2023-12-01 12:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('events', '0010_video_is_vertical'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='max_registrations',
            field=models.IntegerField(blank=True, null=True, verbose_name='maksymalna liczba rejestracji'),
        ),
    ]
