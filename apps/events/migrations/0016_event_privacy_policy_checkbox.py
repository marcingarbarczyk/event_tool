# Generated by Django 4.2.4 on 2024-02-29 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0015_eventbundlecodediscount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='privacy_policy_checkbox',
            field=models.TextField(blank=True, null=True, verbose_name='treść zgody w formularzu'),
        ),
    ]
