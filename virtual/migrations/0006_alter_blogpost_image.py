# Generated by Django 5.0.1 on 2024-02-05 10:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("virtual", "0005_alter_blogpost_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogpost",
            name="image",
            field=models.BinaryField(blank=True, null=True),
        ),
    ]