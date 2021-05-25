# Generated by Django 3.1.7 on 2021-05-24 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caixas', '0002_auto_20210522_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rel_gestor_edificio',
            name='data_fim',
            field=models.DateField(blank=True, default='0000-00-00', null=True),
        ),
        migrations.AlterField(
            model_name='rel_gestor_edificio',
            name='data_inicio',
            field=models.DateField(help_text='Formato: YYYY-MM-DD Exemplo: 2021-12-31'),
        ),
    ]