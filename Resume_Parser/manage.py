#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from django.db import migrations


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Resume_Parser.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()

def seed_skills(apps, schema_editor):
    Skill = apps.get_model('skill_suggestion', 'Skill')
    skills = [
        "Python", "Django", "REST API", "SQL", "Git",
        "Machine Learning", "JavaScript", "React", "HTML", "CSS"
    ]
    for s in skills:
        Skill.objects.get_or_create(name=s)

class Migration(migrations.Migration):

    dependencies = [
        ('skill_suggestion', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_skills),
    ]




