# Generated by Django 4.1.7 on 2023-04-05 18:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_remove_userprofile_first_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='tag',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
