from core.models import Job


def get_all_jobs():
    return Job.objects.all()


def create_job(title, description, employer):
    return Job.objects.create(
        title=title,
        description=description,
        employer=employer
    )
