# Generated by Django 3.2.5 on 2021-08-16 22:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0008_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='model_type',
            field=models.CharField(choices=[('ques', 'Questions'), ('choi', 'Choices')], default='', max_length=4),
            preserve_default=False,
        ),
    ]
