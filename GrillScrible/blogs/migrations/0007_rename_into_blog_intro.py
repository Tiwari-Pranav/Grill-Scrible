# Generated by Django 4.2.3 on 2023-07-11 09:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0006_alter_blog_likes_ip'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='into',
            new_name='intro',
        ),
    ]
