# Generated by Django 2.1.5 on 2019-03-05 21:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bets', '0009_auto_20190305_1105'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usersportbet',
            old_name='ammount',
            new_name='amount',
        ),
    ]
