# Generated by Django 2.1.5 on 2019-03-16 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bets', '0013_futurebet_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='futurebet',
            name='fractional',
            field=models.CharField(default=None, max_length=10),
            preserve_default=False,
        ),
    ]