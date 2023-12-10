# Generated by Django 4.2.7 on 2023-12-09 17:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('snappies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tournee',
            fields=[
                ('id_tournee', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=100, unique=True)),
                ('livreur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]