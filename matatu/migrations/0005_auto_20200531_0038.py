# Generated by Django 3.0.6 on 2020-05-30 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matatu', '0004_auto_20200531_0029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweetobject',
            name='latitude',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='tweetobject',
            name='longitude',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='tweetobject',
            name='route',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
