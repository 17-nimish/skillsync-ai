from django.db import models
from skills.models import Skill

class JobRole(models.Model):
    name = models.CharField(max_length=100)

class RoleSkill(models.Model):
    job = models.ForeignKey(JobRole, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)