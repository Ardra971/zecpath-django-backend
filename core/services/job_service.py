from core.models import Job


def get_all_jobs():
    return Job.objects.all()


def create_job(title, description):
    return Job.objects.create(
        title=title,
        description=description
    )
