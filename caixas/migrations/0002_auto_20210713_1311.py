# Generated by Django 3.1.7 on 2021-07-13 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caixas', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='caixa',
            name='local_atual_id',
        ),
        migrations.AlterField(
            model_name='registo',
            name='codigo_hexa_cartao',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='registo',
            name='codigo_validacao',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='registo',
            name='local_atual_caixa',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='registo',
            name='validado',
            field=models.BooleanField(),
        ),
    ]
