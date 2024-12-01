# Generated by Django 5.1.2 on 2024-12-01 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sbapi', '0004_alter_goalkeeperevent_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='defendingevent',
            name='event_id',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='goalkeeperevent',
            name='event_id',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='passevent',
            name='event_id',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='possessionevent',
            name='event_id',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='shootingevent',
            name='event_id',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='summaryevent',
            name='event_id',
            field=models.BigIntegerField(),
        ),
    ]
