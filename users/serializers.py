from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import normalize_phone_number
from users.models import SpecialistRequest

User = get_user_model()


class SignUpSerializer(serializers.Serializer):
    phone_number = serializers.CharField(trim_whitespace=True)
    password = serializers.CharField(write_only=True, min_length=6)

    def validate_phone_number(self, value):
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("This phone number is already registered.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            phone_number=validated_data["phone_number"],
            password=validated_data["password"],
        )
        return user
    
    
class OTPRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField(trim_whitespace=True)

    def validate_phone_number(self, value):
        return normalize_phone_number(value)


class OTPLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(trim_whitespace=True)
    otp = serializers.CharField(max_length=6, min_length=4)

    def validate_phone_number(self, value):
        return normalize_phone_number(value)

class UserInfoSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source="role.name", allow_null=True)
    
    class Meta:
        model = User
        fields = (
            "id",
            "phone_number",
            "first_name",
            "last_name",
            "full_name",
            "status",
            "role",
            "is_phone_verified",
        )


class SpecialistRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialistRequest
        fields = ("note",)

    def create(self, validated_data):
        user = self.context["request"].user

        sr, created = SpecialistRequest.objects.get_or_create(user=user)
        if "note" in validated_data:
            sr.note = validated_data["note"]
            sr.save(update_fields=["note"])
        return sr


class SpecialistRequestSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = SpecialistRequest
        fields = (
            "id",
            "status",
            "status_display",
            "note",
            "created_at",
            "reviewed_at",
        )
        read_only_fields = fields


class SpecialistRequestAdminDecisionSerializer(serializers.Serializer):
    # approve / reject
    decision = serializers.ChoiceField(choices=("approve", "reject"))
    admin_note = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def validate(self, attrs):
        request_obj: SpecialistRequest = self.context["specialist_request"]
        if request_obj.status != SpecialistRequest.Status.PENDING:
            raise serializers.ValidationError("This request is already reviewed.")
        return attrs