# Generated by Django 4.2.6 on 2024-01-14 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oscarbot', '0004_user_want_action'),
    ]

    operations = [
        migrations.CreateModel(
            name='Constructor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
