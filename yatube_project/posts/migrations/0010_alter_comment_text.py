# Generated by Django 4.2.4 on 2023-08-27 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_post_title_alter_post_author_alter_post_group_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.CharField(max_length=550, verbose_name='Comment'),
        ),
    ]