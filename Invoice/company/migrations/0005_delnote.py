# Generated by Django 2.2.5 on 2019-12-25 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_auto_20191222_1022'),
    ]

    operations = [
        migrations.CreateModel(
            name='DelNote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('del_note_id', models.IntegerField(default=1)),
                ('company_id', models.IntegerField(default=1)),
                ('site_id', models.IntegerField(default=1)),
                ('service', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('units', models.CharField(max_length=300)),
                ('driver', models.CharField(max_length=300)),
            ],
        ),
    ]