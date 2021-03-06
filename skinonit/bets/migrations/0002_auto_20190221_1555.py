# Generated by Django 2.1.5 on 2019-02-21 23:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('win_loss', models.BooleanField(default=None)),
            ],
        ),
        migrations.RemoveField(
            model_name='userbet',
            name='name',
        ),
        migrations.AddField(
            model_name='userbet',
            name='for_against',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userbet',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userbet',
            name='bet',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='bets.Bet'),
            preserve_default=False,
        ),
    ]
