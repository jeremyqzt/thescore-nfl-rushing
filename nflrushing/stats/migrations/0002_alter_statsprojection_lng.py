# Generated by Django 3.2.5 on 2021-07-01 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statsprojection',
            name='lng',
            field=models.CharField(max_length=5),
        ),
    ]
