# Generated by Django 2.1.7 on 2019-03-12 12:24

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Classe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('xp_comp', models.IntegerField(default=0)),
                ('min_silver_comp', models.IntegerField(default=0)),
                ('max_silver_comp', models.IntegerField(default=0)),
                ('cd_comp', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Command',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.CharField(max_length=255)),
                ('how_to', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CommandHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_used', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date de création')),
                ('bonus', models.IntegerField(default=0, null=True)),
                ('command', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.Command')),
            ],
        ),
        migrations.CreateModel(
            name='EventsLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name="Date de l'erreur")),
                ('error', models.TextField()),
                ('command', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('silver', models.IntegerField(default=0)),
                ('bonus_xp', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='GameMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joined_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date de création')),
                ('experience', models.IntegerField(default=0)),
                ('silver', models.IntegerField(default=0)),
                ('token', models.IntegerField(default=0)),
                ('classe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.Classe')),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discord_id', models.CharField(max_length=50, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('joined_at', models.DateTimeField()),
                ('discriminator', models.CharField(max_length=10)),
            ],
        ),

        migrations.CreateModel(
            name='Giveaway',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('participants', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
        ),

        migrations.AddField(
            model_name='gamemember',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.Member', unique=True),
        ),
        migrations.AddField(
            model_name='commandhistory',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.Member'),
        ),
        migrations.AlterUniqueTogether(
            name='commandhistory',
            unique_together={('member', 'command')},
        ),
    ]
