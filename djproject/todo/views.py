from django.shortcuts import redirect
from django.views.generic import TemplateView, FormView,CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout

from todo.forms import TaskForm
from todo.models import Task

# Create your views here.

# def index(request):
#     tasks = Task.objects.all()
#     return render(request,"todo/index.html", {"foo":"cenas", "tasks":tasks})

class TaskListView(LoginRequiredMixin, CreateView):
    login_url = "/signin"
    success_url = "/tasks"
    form_class = TaskForm
    template_name = "todo/task_list.html"

    def get_context_data(self, **kwargs):
        kwargs['object_list'] = Task.objects.filter(user=self.request.user).all()
        return super().get_context_data(**kwargs)    

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class IndexView(TemplateView):
    http_method_names = ['get']	
    template_name = "todo/index.html"

class SignUpView(FormView):
    template_name = "registration/signup.html"
    success_url="/"
    form_class = UserCreationForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("/")