# Generated by Django 2.2.5 on 2020-01-31 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0010_auto_20200131_1821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delnote',
            name='del_note_id',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
