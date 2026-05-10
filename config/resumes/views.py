from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Resume
from .utils import extract_text

from skills.models import Skill
from skills.extractor import extract_skills

from jobs.models import JobRole, RoleSkill

from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


# ================================
# 🔥 AI ROADMAP GENERATOR
# ================================
def generate_ai_roadmap(missing_skills):

    SKILL_CATEGORIES = {
        "programming": ["python", "java", "c++"],
        "web": ["html", "css", "javascript", "react", "django"],
        "database": ["sql", "mongodb"],
        "ai": ["machine learning", "deep learning", "nlp"],
        "tools": ["git", "docker"]
    }

    roadmap = {
        "Beginner": [],
        "Intermediate": [],
        "Advanced": []
    }

    for skill in missing_skills:
        for category, skills in SKILL_CATEGORIES.items():
            if skill in skills:

                roadmap["Beginner"].append(f"Learn basics of {skill}")
                roadmap["Intermediate"].append(f"Build projects using {skill}")
                roadmap["Advanced"].append(f"Master advanced concepts of {skill}")

    return roadmap


# ================================
# 🔥 JOB ROLE SUGGESTION
# ================================
def suggest_roles(user_skills):

    role_scores = []
    roles = JobRole.objects.all()

    for role in roles:
        required_skills = list(
            RoleSkill.objects.filter(job=role)
            .values_list('skill__name', flat=True)
        )

        required_skills = [s.lower() for s in required_skills]

        match = len(set(user_skills) & set(required_skills))

        role_scores.append((role.name, match))

    role_scores.sort(key=lambda x: x[1], reverse=True)

    return role_scores[:3]


# ================================
# 🔥 MAIN VIEW
# ================================
@login_required
def upload_resume(request):

    roles = JobRole.objects.all()

    if request.method == 'POST':

        file = request.FILES.get('resume')
        selected_role = request.POST.get('role')

        if not selected_role:
            return render(request, 'upload.html', {
                'roles': roles,
                'error': 'Please select a job role'
            })

        try:
            role = JobRole.objects.get(id=selected_role)
        except JobRole.DoesNotExist:
            return render(request, 'upload.html', {
                'roles': roles,
                'error': 'Invalid role selected'
            })

        if request.user.is_authenticated:
            Resume.objects.create(user=request.user, file=file)

        text = extract_text(file)

        skill_list = list(Skill.objects.values_list('name', flat=True))

        user_skills = extract_skills(text, skill_list)

        required_skills = list(
            RoleSkill.objects.filter(job=role)
            .values_list('skill__name', flat=True)
        )

        required_skills = [skill.lower() for skill in required_skills]

        matched = set(user_skills) & set(required_skills)

        match = (len(matched) / len(required_skills)) * 100 if required_skills else 0

        missing = set(required_skills) - set(user_skills)

        # 🔥 ROADMAP
        roadmap = generate_ai_roadmap(missing)

        # 🔥 ROLE SUGGESTION
        suggested_roles = suggest_roles(user_skills)

        recommendations = {
            'python': 'Learn Python from freeCodeCamp',
            'django': 'Build Django projects',
            'sql': 'Practice SQL on LeetCode',
            'javascript': 'Learn JS from MDN Docs',
            'html': 'Practice HTML basics',
            'css': 'Learn CSS Flexbox and Grid',
            'java': 'Learn Java OOP concepts',
            'salesforce': 'Learn Salesforce from Trailhead',
            'lwc': 'Learn LWC from Trailhead',
            'salesforce admin': 'Learn Salesforce admin from Trailhead',
        }

        suggestions = [
            recommendations.get(skill, "Learn this skill")
            for skill in missing
        ]

        # 🔥 SAVE DATA FOR PDF
        request.session['skills'] = list(user_skills)
        request.session['matched'] = list(matched)
        request.session['missing'] = list(missing)
        request.session['match'] = round(match, 2)

        return render(request, 'upload.html', {
            'roles': roles,
            'skills': user_skills,
            'match': round(match, 2),
            'matched': matched,
            'missing': missing,
            'suggestions': suggestions,
            'roadmap': roadmap,
            'suggested_roles': suggested_roles
        })

    return render(request, 'upload.html', {
        'roles': roles
    })


# ================================
# 📄 DOWNLOAD PDF REPORT
# ================================


@login_required
def download_report(request):

    # 🔥 get data from session
    skills = request.session.get('skills', [])
    matched = request.session.get('matched', [])
    missing = request.session.get('missing', [])
    match = request.session.get('match', 0)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="SkillSync_Report.pdf"'

    doc = SimpleDocTemplate(response)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("SkillSync AI Report", styles['Title']))
    content.append(Spacer(1, 20))

    content.append(Paragraph(f"Match Score: {match}%", styles['Heading2']))
    content.append(Spacer(1, 10))

    content.append(Paragraph("Extracted Skills:", styles['Heading3']))
    for s in skills:
        content.append(Paragraph(f"- {s}", styles['Normal']))

    content.append(Spacer(1, 10))

    content.append(Paragraph("Matched Skills:", styles['Heading3']))
    for s in matched:
        content.append(Paragraph(f"- {s}", styles['Normal']))

    content.append(Spacer(1, 10))

    content.append(Paragraph("Missing Skills:", styles['Heading3']))
    for s in missing:
        content.append(Paragraph(f"- {s}", styles['Normal']))

    doc.build(content)

    return response