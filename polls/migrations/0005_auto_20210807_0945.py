# Generated by Django 3.2.5 on 2021-08-07 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_choices_sort_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionnaires',
            name='q11',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='questionnaires',
            name='q12',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='questionnaires',
            name='q13',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='questionnaires',
            name='q14',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='questionnaires',
            name='q15',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='questionnaires',
            name='q16',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='questionnaires',
            name='q17',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='questionnaires',
            name='q18',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='questionnaires',
            name='q19',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='questionnaires',
            name='q20',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='questionnaires',
            name='q1',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='questionnaires',
            name='q10',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='questionnaires',
            name='q2',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='questionnaires',
            name='q3',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='questionnaires',
            name='q4',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='questionnaires',
            name='q5',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='questionnaires',
            name='q6',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='questionnaires',
            name='q7',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='questionnaires',
            name='q8',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='questionnaires',
            name='q9',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
