# Generated by Django 5.2.1 on 2025-05-24 05:45

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roadmap', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_message', models.TextField(help_text='The message sent by the user.')),
                ('llm_response', models.TextField(blank=True, help_text='The response generated by the LLM.', null=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, help_text='The time the message was created.')),
                ('subtopic', models.ForeignKey(help_text='The subtopic this chat message belongs to.', on_delete=django.db.models.deletion.CASCADE, related_name='chat_messages', to='roadmap.subtopic')),
            ],
            options={
                'ordering': ['timestamp'],
            },
        ),
    ]
