# Generated by Django 3.2.5 on 2021-08-13 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_auto_20210813_1239'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveys',
            name='end_text',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
