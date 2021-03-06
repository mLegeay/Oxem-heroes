# Generated by Django 2.1.7 on 2019-02-28 13:36

from django.db import migrations, models

from oxemHeroes.classe.models import Classe


def add_commands(apps, schema_editor):
    """Mise en places des commandes dans la BDD."""

    Classe.objects.create(name="oxem", xp_comp=10, min_silver_comp=20, max_silver_comp=40, cd_comp=60)
    Classe.objects.create(name="talkoran", xp_comp=20, min_silver_comp=25, max_silver_comp=30, cd_comp=40)
    Classe.objects.create(name="shosizuke", xp_comp=8, min_silver_comp=10, max_silver_comp=25, cd_comp=25)


class Migration(migrations.Migration):

    dependencies = [
        ('classe', '0001_initial')
    ]

    operations = [
        migrations.RunPython(add_commands)
    ]
