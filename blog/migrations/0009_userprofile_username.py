# Generated by Django 4.1.7 on 2023-04-04 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_userprofile_first_name_userprofile_last_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='username',
            field=models.CharField(max_length=60, null=True, unique=True),
        ),
    ]