# Generated by Django 3.2.5 on 2021-08-08 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_alter_post_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(max_length=1200, null=True),
        ),
        migrations.AlterField(
            model_name='reply',
            name='text',
            field=models.TextField(max_length=1200, null=True),
        ),
    ]
