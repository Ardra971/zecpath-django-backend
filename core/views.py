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


class JobListAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        jobs = get_all_jobs()
        serializer = JobSerializer(jobs, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


class JobCreateAPI(APIView):
    def post(self, request):
        serializer = JobSerializer(data=request.data)

        if serializer.is_valid():
            job = create_job(
                title=serializer.validated_data["title"],
                description=serializer.validated_data["description"]
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