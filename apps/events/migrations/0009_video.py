# Generated by Django 4.2.4 on 2023-11-03 10:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('events', '0008_event_x_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=0, verbose_name='kolejność')),
                ('iframe_url', models.URLField(verbose_name='adres url')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='videos/', verbose_name='miniatura')),
            ],
            options={
                'verbose_name': 'video',
                'verbose_name_plural': 'video',
                'ordering': ['order'],
                'abstract': False,
            },
        ),
    ]
