from django.db.migrations import serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.services.job_service import get_all_jobs, create_job
from .models import User, Job
from .serializers import (
    UserSerializer,
    JobSerializer,
    UserRegistrationSerializer,
    RegisterSerializer
)
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsEmployer
from core.permissions import IsAdmin
from .models import User, Job, Application
from core.permissions import IsEmployer, IsAdmin, IsCandidate
from core.models import User, Job, Application, Candidate, Employer
from core.serializers import CandidateProfileSerializer, EmployerProfileSerializer
from rest_framework.parsers import MultiPartParser, FormParser


class JobListAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        jobs = get_all_jobs()
        serializer = JobSerializer(jobs, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


class JobCreateAPI(APIView):
    permission_classes = [IsEmployer]
    def post(self, request):
        serializer = JobSerializer(data=request.data)

        if serializer.is_valid():
            job = create_job(
                title=serializer.validated_data["title"],
                description=serializer.validated_data["description"],
                employer=request.user.employer
            )
            return Response(
                JobSerializer(job).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UserTestAPI(APIView):
    permission_classes = [IsAdmin]
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class JobDeleteAPI(APIView):
    def delete(self, request, pk):
        try:
            job = Job.objects.get(pk=pk)
            job.delete()
            return Response(
                {"message": "Job deleted successfully"},
                status=status.HTTP_204_NO_CONTENT
            )
        except Job.DoesNotExist:
            return Response(
                {"error": "Job not found"},
                status=status.HTTP_404_NOT_FOUND
            )

class UserRegistrationAPI(APIView):

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            return Response(
                UserSerializer(user).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class RegisterAPI(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            return Response(
                {
                    "message": "User registered successfully",
                    "user": RegisterSerializer(user).data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class ApplicationCreateAPI(APIView):
    permission_classes = [IsCandidate]

    def post(self, request):
        job_id = request.data.get("job")

        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return Response(
                {"error": "Job not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        application = Application.objects.create(
            user=request.user,
            job=job
        )

        return Response(
            {
                "message": "Application submitted successfully",
                "application_id": application.id
            },
            status=status.HTTP_201_CREATED
        )

class CandidateProfileAPI(APIView):
    permission_classes = [IsCandidate]

    def get(self, request):
        profile = request.user.candidate

        if profile.is_deleted:
            return Response(
                {"error": "Profile has been deleted"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CandidateProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        profile = request.user.candidate

        if profile.is_deleted:
            return Response(
                {"error": "Profile has been deleted"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CandidateProfileSerializer(
            profile,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request):
        profile = request.user.candidate

        if profile.is_deleted:
            return Response(
                {"error": "Profile already deleted"},
                status=status.HTTP_404_NOT_FOUND
            )

        from django.utils import timezone

        profile.is_deleted = True
        profile.deleted_at = timezone.now()
        profile.save()

        return Response(
            {"message": "Candidate profile deleted successfully"},
            status=status.HTTP_200_OK
        )

class EmployerProfileAPI(APIView):
    permission_classes = [IsEmployer]

    def get(self, request):
        profile = request.user.employer

        if profile.is_deleted:
            return Response(
                {"error": "Profile has been deleted"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = EmployerProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        profile = request.user.employer

        if profile.is_deleted:
            return Response(
                {"error": "Profile has been deleted"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = EmployerProfileSerializer(
            profile,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request):
        profile = request.user.employer

        if profile.is_deleted:
            return Response(
                {"error": "Profile already deleted"},
                status=status.HTTP_404_NOT_FOUND
            )

        from django.utils import timezone

        profile.is_deleted = True
        profile.deleted_at = timezone.now()
        profile.save()

        return Response(
            {"message": "Employer profile deleted successfully"},
            status=status.HTTP_200_OK
        )

class AdminProfileListAPI(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        candidates = Candidate.objects.filter(is_deleted=False)
        employers = Employer.objects.filter(is_deleted=False)

        candidate_serializer = CandidateProfileSerializer(
            candidates,
            many=True
        )

        employer_serializer = EmployerProfileSerializer(
            employers,
            many=True
        )

        return Response(
            {
                "candidates": candidate_serializer.data,
                "employers": employer_serializer.data
            },
            status=status.HTTP_200_OK
        )

class ResumeUploadAPI(APIView):
    permission_classes = [IsCandidate]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        profile = request.user.candidate

        if profile.is_deleted:
            return Response(
                {"error": "Profile has been deleted"},
                status=status.HTTP_404_NOT_FOUND
            )

        uploaded_file = request.FILES.get("resume")

        if not uploaded_file:
            return Response(
                {"error": "No resume file was uploaded."},
                status=status.HTTP_400_BAD_REQUEST
            )

        old_resume_name = profile.resume.name

        # Validate the uploaded file
        serializer = CandidateProfileSerializer(
            profile,
            data={"resume": uploaded_file},
            partial=True
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get the validated file
        # Get the validated file
        new_resume = serializer.validated_data["resume"]

        # Save the new resume explicitly
        profile.resume.save(
            new_resume.name,
            new_resume,
            save=True
        )

        # Reload profile from database
        profile.refresh_from_db()

        # Delete the old resume after successful replacement
        if old_resume_name and old_resume_name != profile.resume.name:
            from django.core.files.storage import default_storage
            if default_storage.exists(old_resume_name):
                default_storage.delete(old_resume_name)

        return Response(
            {
                "message": "Resume uploaded successfully",
                "resume": profile.resume.url
            },
            status=status.HTTP_200_OK
        )