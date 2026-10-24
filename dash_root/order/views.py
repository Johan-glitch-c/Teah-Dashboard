from django.shortcuts import render
from .models import Task
from users.models import User
from django.contrib.auth import get_user
# Create your views here.
def index(request):
    users_count = User.objects.count()
    users = User.objects.all()
    User_now = get_user(request)
    tasks = Task.objects.filter(person_to_do=User_now)
    opened_tasks = Task.objects.filter(opened=True)
    count_open_tasks = opened_tasks.count()

    if Task.objects.filter(status="DN", person_to_do=User_now) == []:
        completed_tasks = 0
    else:
        completed_tasks =  Task.objects.filter(status="DN", person_to_do=User_now).count


    context = {
        'tasks':tasks,
        "opened_tasks": opened_tasks,
        "count_open_tasks": count_open_tasks,
        "completed_tasks": completed_tasks,
        "users_count":users_count,
        "users": users
    }
    return render(request, 'index.html', context)