# Generated by Django 3.2.5 on 2021-08-04 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20210803_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='choices',
            name='choice_key',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]
