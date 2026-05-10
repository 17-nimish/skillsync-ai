from django.http import HttpResponse
from django.shortcuts import render
from jobs.models import JobRole, RoleSkill

def home(request):
    return render(request, 'home.html')

def match_result(request, user_skills):
    role = JobRole.objects.get(name="Backend Developer")

    required_skills = list(
        RoleSkill.objects.filter(job=role)
        .values_list('skill__name', flat=True)
    )

    required_skills = [skill.lower() for skill in required_skills]

    # Matching
    matched = set(user_skills) & set(required_skills)

    match_percent = (len(matched) / len(required_skills)) * 100

    # Missing skills
    missing = set(required_skills) - set(user_skills)

    return {
        'match': round(match_percent, 2),
        'matched': matched,
        'missing': missing,
        'required': required_skills
    }