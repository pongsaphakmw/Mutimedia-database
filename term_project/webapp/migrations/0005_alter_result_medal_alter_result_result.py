# Generated by Django 4.0 on 2024-03-01 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_alter_result_rank_alter_result_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='medal',
            field=models.CharField(choices=[('Gold', 'Gold'), ('Silver', 'Silver'), ('Bronze', 'Bronze'), ('None', 'None')], default='None', max_length=10),
        ),
        migrations.AlterField(
            model_name='result',
            name='result',
            field=models.CharField(default='On Going', max_length=50),
        ),
    ]
