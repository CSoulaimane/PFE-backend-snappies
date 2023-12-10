# Generated by Django 4.2.7 on 2023-12-10 18:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('snappies', '0011_rename_nbr_caisse_caisse_commande_nbr_caisses_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caisse_commande',
            name='caisse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='snappies.caisse'),
        ),
        migrations.AlterField(
            model_name='caisse_commande',
            name='commande',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='snappies.commande'),
        ),
    ]
