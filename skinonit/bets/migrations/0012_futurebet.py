# Generated by Django 2.1.5 on 2019-03-16 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bets', '0011_usersportbet_odds'),
    ]

    operations = [
        migrations.CreateModel(
            name='FutureBet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField()),
                ('description', models.CharField(max_length=200)),
                ('american', models.IntegerField(default=0)),
                ('decimal', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
    ]