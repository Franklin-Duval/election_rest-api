# Generated by Django 3.1.2 on 2020-11-23 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aspy_election', '0003_auto_20201107_2253'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aspians',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matricule', models.CharField(max_length=10, unique=True)),
            ],
        ),
    ]
