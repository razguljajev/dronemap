# Generated by Django 5.1.1 on 2024-10-04 06:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Drone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='dronedata',
            name='drone',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='data', to='map.drone'),
            preserve_default=False,
        ),
    ]
