# Generated by Django 2.2 on 2020-04-10 05:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0005_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpost',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='forum.Author'),
        ),
    ]
