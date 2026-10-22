from django.db import models

# Create your models here.

# class Status(models.Model):

#     ...


# class Priority(models.Model):
#     ...


# class Task(models.Model):
#     name = models.CharField(max_length= 70, blank = False, null = False)
#     description = models.TextField(blank= False, null = False)
#     status = models.ForeignKey(on_delete=CASCADE)
#     priority = models.ForeignKey(on_delete=CASCADE)
#     started_dat = models.DateTimeField(auto_now_add=True)
#     deadline = models.DateTimeField(blank=False, null=False)
#     author = ...
#     person_to_do = ...
    

#     def __str__():
#         return self.name

#     class Meta:
#         verbose_name = "Task"
#         verbose_name_plural = "Tasks"