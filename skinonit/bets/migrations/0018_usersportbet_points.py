# Generated by Django 2.1.5 on 2019-06-10 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bets', '0017_auto_20190606_1526'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersportbet',
            name='points',
            field=models.FloatField(default=0),
        ),
    ]
