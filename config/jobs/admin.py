from django.contrib import admin
from .models import JobRole, RoleSkill

@admin.register(JobRole)
class JobRoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(RoleSkill)
class RoleSkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'job', 'skill')
    list_filter = ('job',)