# Generated by Django 5.2 on 2025-07-08 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meu_app', '0006_tarefaform'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TarefaForm',
        ),
        migrations.AddField(
            model_name='tarefa',
            name='data',
            field=models.DateField(blank=True, null=True),
        ),
    ]
