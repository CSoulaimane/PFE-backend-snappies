# Generated by Django 4.2.7 on 2023-12-09 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snappies', '0006_caisse_commande'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commande',
            name='id_commande',
            field=models.AutoField(max_length=50, primary_key=True, serialize=False),
        ),
    ]