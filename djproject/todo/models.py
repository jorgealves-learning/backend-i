from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Task(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.TextField()
    description = models.TextField()
    due_date = models.DateField(null=True)
    is_done = models.BooleanField(null=False,blank=False,default=False)
    user = models.ForeignKey(get_user_model(),on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "todo_tasks"
        verbose_name = "Task"
        verbose_name_plural = "Tasks"