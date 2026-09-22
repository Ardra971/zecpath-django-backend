from rest_framework import serializers
from .models import User, Job, Application, Candidate, Employer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'
class UserRegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    class Meta:
        model = User
        fields = (
            "name",
            "email",
            "phone",
            "password",
            "role",
        )
        extra_kwargs = {
            "role": {
                "required": True
            }
        }

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = User.objects.create_user(
            password=password,
            **validated_data
        )

        return user

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["name", "email", "phone", "password", "role"]

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = User.objects.create_user(
            password=password,
            **validated_data
        )

        return user

class CandidateProfileSerializer(serializers.ModelSerializer):

    def validate_resume(self, value):
        allowed_extensions = [".pdf", ".doc", ".docx"]

        file_name = value.name.lower()

        # Check file extension
        if not any(file_name.endswith(ext) for ext in allowed_extensions):
            raise serializers.ValidationError(
                "Only PDF, DOC, and DOCX files are allowed."
            )

        # Check MIME/content type
        allowed_content_types = [
            "application/pdf",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ]

        if value.content_type not in allowed_content_types:
            raise serializers.ValidationError(
                "Invalid resume file type."
            )

        # Check file size - 5 MB
        max_size = 5 * 1024 * 1024

        if value.size > max_size:
            raise serializers.ValidationError(
                "Resume file size must not exceed 5 MB."
            )

        return value

    class Meta:
        model = Candidate
        fields = [
            "id",
            "phone",
            "skills",
            "education",
            "experience",
            "expected_salary",
            "resume_text",
            "resume",
        ]
        read_only_fields = ["id"]

    def validate_expected_salary(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError(
                "Expected salary cannot be negative."
            )
        return value


class EmployerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = [
            "id",
            "company_name",
            "company_description",
            "company_website",
            "company_location",
        ]
        read_only_fields = ["id"]