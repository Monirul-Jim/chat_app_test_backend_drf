# Generated by Django 5.1.1 on 2024-09-30 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signup_login', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='room',
        ),
        migrations.RemoveField(
            model_name='message',
            name='audio',
        ),
        migrations.RemoveField(
            model_name='message',
            name='document',
        ),
        migrations.RemoveField(
            model_name='message',
            name='image',
        ),
        migrations.RemoveField(
            model_name='message',
            name='video',
        ),
        migrations.AddField(
            model_name='message',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='uploads/'),
        ),
        migrations.AddField(
            model_name='message',
            name='message_type',
            field=models.CharField(choices=[('text', 'Text'), ('emoji', 'Emoji'), ('audio', 'Audio'), ('video', 'Video'), ('file', 'File')], default='text', max_length=10),
        ),
        migrations.DeleteModel(
            name='ChatRoom',
        ),
    ]
