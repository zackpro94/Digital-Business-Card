# Generated by Django 5.1.7 on 2025-03-16 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='businesscard',
            name='theme',
            field=models.CharField(choices=[('default', 'Default'), ('elegant', 'Elegant'), ('modern', 'Modern')], default='default', max_length=20),
        ),
    ]
