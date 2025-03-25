from django.contrib import admin

from todo.models import Task

# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id","title","description", "due_date","is_done")
    list_editable = ("due_date","is_done")
    sortable_by = ("due_date","is_done", "title")

admin.site.register(Task,TaskAdmin)