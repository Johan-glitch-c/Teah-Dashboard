from django.db import models, transaction
from django.db.models import Sum
from users.models import User
from django.core.validators import MinValueValidator
from django.utils.text import slugify
from decimal import Decimal

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
    description = models.TextField(blank=True)
    status = models.CharField(max_length=2, choices= STATUS,default="ST")
    priority = models.CharField(max_length=2, choices=PRIORITY, default='LW')
    opened = models.BooleanField(default=True)
    started_dat = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    author = models.ForeignKey(User,on_delete=models.CASCADE, related_name="created_tasks")
    person_to_do = models.ForeignKey(User,on_delete=models.CASCADE, related_name="tasks")
    hours_of_work = models.DecimalField(max_digits = 4, decimal_places=2, default=0,validators=[MinValueValidator(0)])
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            super().save(*args, **kwargs)
            self.slug = slugify(self.id)
            return super().save(update_fields=['slug'])
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

class Record(models.Model):
    description = models.CharField(max_length=200, blank=True, null=True)
    task_name = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_depend')
    hours = models.DecimalField(max_digits=4, decimal_places=2, default= 0, validators=[MinValueValidator(0)])
    person = models.ForeignKey(User, on_delete=models.CASCADE, related_name='person_doing')


    @staticmethod
    def update_tasks_hours(task_id):
        total = Record.objects.filter(task_name_id=task_id).aggregate(total = Sum('hours'))['total']
        Task.objects.filter(pk = task_id).update(
            hours_of_work=total if total is not None else Decimal('0.00')
        )
        
    @transaction.atomic
    def save(self, *args, **kwargs):
        old_data = None

        if self.pk:
            old_data = Record.objects.filter(
                pk=self.pk
            ).values('task_name_id').first()

        task_ids = {self.task_name_id}

        if old_data:
            task_ids.add(old_data['task_name_id'])

        list(
            Task.objects.select_for_update()
            .filter(pk__in=task_ids)
            .order_by('pk')
        )

        super().save(*args, **kwargs)

        for task_id in task_ids:
            self.update_tasks_hours(task_id)

    @transaction.atomic
    def delete(task_id):
        old_data = None

        if self.pk:
            old_data = Record.objects.filter(
                pk=self.pk
            ).values('task_name_id').first()

            if old_data:
                task_id = old_data['task_name_id']

                Task.objects.select_for_update().filter(pk = task_id).first()

                super().delete(*args, **kwargs)

                self.update_tasks_hours(task_id)
                return
        
            super().delete(*args, **kwargs)


    def __str__(self):
        return str(self.id)