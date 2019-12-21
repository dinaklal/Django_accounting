# Generated by Django 2.2.5 on 2019-09-28 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('home', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sites',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('Unit_price', models.CharField(max_length=100)),
                ('Description', models.CharField(default='Site', max_length=500)),
            ],
        ),
    ]
