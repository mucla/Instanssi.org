# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-09 00:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ext_programme', '0002_auto_20150403_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programmeevent',
            name='icon2_original',
            field=models.ImageField(blank=True, help_text='Kuva 2 tapahtumalle.', upload_to='programme/images/', verbose_name='Kuva 2'),
        ),
        migrations.AlterField(
            model_name='programmeevent',
            name='icon_original',
            field=models.ImageField(blank=True, help_text='Kuva 1 tapahtumalle.', upload_to='programme/images/', verbose_name='Kuva 1'),
        ),
    ]