from django.db import models
from users.models import User
from django.core.validators import MinValueValidator
# Create your models here.



class Task(models.Model):
    STATUS = {
    "ST" : "К выполнению",
    'PG': "В процессе",
    "DN": "Выполнено",
    "DD": "Просрочено"
}

    PRIORITY={
    "LW": "Низкий",
    "MD": "Средний",
    "HG": "Высокий",
    "CR": "Критично"
}

    name = models.CharField(max_length= 70)
    description = models.TextField()
    status = models.CharField(max_length=2, choices= STATUS,default="ST")
    priority = models.CharField(max_length=2, choices=PRIORITY, default='LW')
    started_dat = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    author = models.ForeignKey(User,on_delete=models.CASCADE, related_name="created_tasks")
    person_to_do = models.ForeignKey(User,on_delete=models.CASCADE, related_name="tasks")
    hours_of_work = models.DecimalField(max_digits = 4, decimal_places=2, default=0,validators=[MinValueValidator(0)])
    

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"