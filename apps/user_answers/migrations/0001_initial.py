# Generated by Django 4.2.4 on 2024-06-24 15:08

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0005_info_alter_registrationdata_area_and_more'),
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Testing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started_at', models.DateTimeField(verbose_name='started at')),
                ('finished_at', models.DateTimeField(verbose_name='finished at')),
                ('spent_time', models.TimeField(default=datetime.timedelta(seconds=3600), verbose_name='spent time')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('correct_answers_count', models.IntegerField(default=0, verbose_name='correct answers')),
                ('tg_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.telegramuser', verbose_name='telegram user')),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.tour', verbose_name='tour')),
            ],
            options={
                'verbose_name': 'testing',
                'verbose_name_plural': 'testings',
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('received_answer', models.CharField(max_length=200, verbose_name='received answer')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.question', verbose_name='question')),
                ('testing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_answers.testing', verbose_name='testing')),
                ('tg_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.telegramuser', verbose_name='telegram user')),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.tour', verbose_name='tour')),
            ],
            options={
                'verbose_name': 'answer',
                'verbose_name_plural': 'answers',
            },
        ),
    ]
