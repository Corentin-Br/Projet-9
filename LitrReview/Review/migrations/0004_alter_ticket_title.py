# Generated by Django 3.2.4 on 2021-07-02 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Review', '0003_alter_ticket_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='title',
            field=models.CharField(max_length=128, verbose_name='Titre'),
        ),
    ]