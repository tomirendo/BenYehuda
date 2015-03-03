# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='piece',
            name='date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='piece',
            name='translator',
            field=models.ForeignKey(blank=True, to='main.Translator', null=True),
        ),
        migrations.AlterField(
            model_name='translator',
            name='death',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='translator',
            name='wikipedia_link',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
