# Generated by Django 3.2.9 on 2021-11-29 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='botusers',
            name='user_id',
            field=models.CharField(default=4484684684, max_length=50),
            preserve_default=False,
        ),
    ]
