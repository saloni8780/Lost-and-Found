# Generated by Django 5.1.6 on 2025-04-13 12:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LostFoundItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('item_type', models.CharField(choices=[('Lost', 'Lost'), ('Found', 'Found')], max_length=5)),
                ('location', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='items/')),
                ('posted_at', models.DateTimeField(auto_now_add=True)),
                ('posted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
