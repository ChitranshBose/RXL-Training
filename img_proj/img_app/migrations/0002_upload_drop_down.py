# Generated by Django 4.1 on 2024-06-27 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('img_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='upload',
            name='drop_down',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], default=1),
        ),
    ]
