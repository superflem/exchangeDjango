# Generated by Django 4.0.5 on 2022-06-25 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0003_alter_utente_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utente',
            name='password',
            field=models.CharField(max_length=128),
        ),
    ]
