# Generated by Django 4.2.4 on 2023-09-05 11:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UsersCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, default=None, max_length=9)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='code_of_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': "User's code",
                'verbose_name_plural': "Users' codes",
            },
        ),
    ]
