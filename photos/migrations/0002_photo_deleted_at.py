# Generated by Django 3.2.16 on 2023-05-16 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='deleted_at',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
