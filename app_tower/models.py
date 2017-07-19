# -*- coding: utf-8 -*
from django.db import models

# Create your models here.
#主机清单
class inventories(models.Model):
    name=models.CharField(max_length=32)
    description = models.CharField(max_length=128)

    def __str__(self):
        return self.name, self.description

#主机
class host(models.Model):
    group=models.CharField(max_length=32)
    name=models.CharField(max_length=32)
    description = models.CharField(max_length=128)
    inventories_id = models.ForeignKey(inventories)

#任务模板
class jobTemplate(models.Model):
    name=models.CharField(max_length=32)
    description = models.CharField(max_length=128)
    inventories_id = models.ForeignKey(inventories)
   # project_id = models.ForeignKey(project)
    user=models.CharField(max_length=32)
    playbook=models.CharField(max_length=1024)