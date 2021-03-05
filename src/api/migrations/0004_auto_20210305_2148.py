# Generated by Django 3.1.7 on 2021-03-05 18:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0003_auto_20210303_1904'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='teacher',
        ),
        migrations.RemoveField(
            model_name='course',
            name='user',
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_comment', to='auth.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='creator',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='creator', to='auth.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(related_name='course_students', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='teachers',
            field=models.ManyToManyField(related_name='course_teachers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='lecture',
            name='creator',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='lecture_creator', to='auth.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='mark',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='teacher_mark', to=settings.AUTH_USER_MODEL),
        ),
    ]