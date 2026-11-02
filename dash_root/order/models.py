from django.db import models
from users.models import User
from django.core.validators import MinValueValidator
from django.utils.text import slugify
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