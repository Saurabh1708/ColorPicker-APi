# Generated by Django 3.0.3 on 2021-01-07 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Picker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dominant_color', models.CharField(max_length=30)),
                ('logo_border', models.CharField(max_length=30)),
                ('url', models.URLField()),
            ],
        ),
    ]