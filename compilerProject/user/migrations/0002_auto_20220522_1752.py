# Generated by Django 2.2.8 on 2022-05-22 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='group',
            field=models.CharField(default=None, max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='surname',
            field=models.CharField(default=None, max_length=32),
            preserve_default=False,
        ),
    ]
