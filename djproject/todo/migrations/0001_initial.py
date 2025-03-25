# Generated by Django 5.1.7 on 2025-03-20 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Task",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("title", models.TextField()),
                ("description", models.TextField()),
                ("due_date", models.DateField(null=True)),
                ("is_done", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name": "Task",
                "verbose_name_plural": "Tasks",
                "db_table": "todo_tasks",
            },
        ),
    ]
