# Generated by Django 2.1.7 on 2019-03-12 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0006_auto_20190311_1153'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamemember',
            name='token',
            field=models.IntegerField(default=0),
        ),
    ]
