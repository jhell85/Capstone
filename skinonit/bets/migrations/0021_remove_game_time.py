# Generated by Django 2.1.5 on 2019-06-12 22:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bets', '0020_game'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='time',
        ),
    ]
