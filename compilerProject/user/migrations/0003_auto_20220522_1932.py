# Generated by Django 2.2.8 on 2022-05-22 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20220522_1752'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.IntegerField(choices=[(1, 'Admin'), (0, 'User')], default=0),
        ),
    ]
