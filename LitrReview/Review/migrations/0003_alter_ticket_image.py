# Generated by Django 3.2.4 on 2021-07-01 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Review', '0002_alter_ticket_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
