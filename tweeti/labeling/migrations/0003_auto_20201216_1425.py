# Generated by Django 3.1.3 on 2020-12-16 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labeling', '0002_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='id_str',
            field=models.CharField(blank=True, help_text='id of original tweet', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='tweet',
            name='status',
            field=models.CharField(blank=True, help_text='statud of the tweet, for example inactive', max_length=255, null=True),
        ),
    ]
