# Generated by Django 4.0 on 2024-03-02 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_alter_result_medal_alter_result_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classification',
            name='classification_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='classification',
            name='classification_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
