# Generated by Django 2.2.5 on 2020-01-27 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0008_delnote_inv_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='starting_balance',
            field=models.FloatField(default=0.0, max_length=20),
        ),
    ]