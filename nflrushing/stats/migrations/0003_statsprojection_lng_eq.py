# Generated by Django 3.2.5 on 2021-07-01 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0002_alter_statsprojection_lng'),
    ]

    operations = [
        migrations.AddField(
            model_name='statsprojection',
            name='lng_eq',
            field=models.IntegerField(default=0),
        ),
    ]
