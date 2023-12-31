# Generated by Django 4.2.4 on 2023-09-06 09:54

import ckeditor_uploader.fields
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
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_creation', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(help_text='Up to 255 symbols', max_length=255)),
                ('category', models.CharField(choices=[('TA', 'Танки'), ('HL', 'Хилы'), ('DD', 'ДД'), ('TR', 'Торговцы'), ('GM', 'Гилдмастеры'), ('QG', 'Квестгиверы'), ('SM', 'Кузнецы'), ('TN', 'Кожевники'), ('PT', 'Зельевары'), ('SP', 'Мастера заклинаний')], default=None, max_length=15)),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(blank=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Пост',
                'verbose_name_plural': 'Посты',
            },
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_creation', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField(blank=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('is_rejected', models.BooleanField(default=False)),
                ('adv', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies_to_post', to='adverts.post')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reply_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Ответ',
                'verbose_name_plural': 'Ответы',
            },
        ),
    ]
