# Generated by Django 3.2.4 on 2021-07-01 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Review', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
