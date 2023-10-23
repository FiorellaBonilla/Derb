# Generated by Django 4.2.5 on 2023-10-22 20:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_model', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResponseForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('responseF', models.TextField(blank=True, null=True)),
                ('fieldsRes', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api_model.modelfields')),
            ],
        ),
    ]
