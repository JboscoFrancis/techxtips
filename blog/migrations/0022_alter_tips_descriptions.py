# Generated by Django 3.2.5 on 2021-08-20 12:57

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0021_alter_tips_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tips',
            name='descriptions',
            field=ckeditor.fields.RichTextField(max_length=2400, null=True),
        ),
    ]
