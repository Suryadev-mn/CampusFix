from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from .models import User
from apps.departments.serializers import DepartmentSerializer
from apps.departments.models import Department

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['role'] = user.role
        token['name'] = user.get_full_name() or user.username
        if user.department:
            token['department_id'] = user.department.id
            token['department_name'] = user.department.name
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'id': self.user.id,
            'email': self.user.email,
            'username': self.user.username,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'role': self.user.role,
            'phone': self.user.phone,
            'identifier': self.user.identifier,
            'department': DepartmentSerializer(self.user.department).data if self.user.department else None,
            'avatar': self.user.avatar.url if self.user.avatar else None,
        }
        return data


class DepartmentRelatedField(serializers.PrimaryKeyRelatedField):
    def to_internal_value(self, data):
        if isinstance(data, str) and not data.isdigit():
            dept = Department.objects.filter(code__iexact=data).first()
            if dept:
                return dept
            dept = Department.objects.filter(name__icontains=data).first()
            if dept:
                return dept
        return super().to_internal_value(data)


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)
    department_id = DepartmentRelatedField(
        queryset=Department.objects.all(), source='department', required=False, allow_null=True
    )

    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'password', 'password_confirm',
            'first_name', 'last_name', 'role', 'phone', 'identifier', 'department_id'
        ]
        extra_kwargs = {
            'username': {'required': False},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, attrs):
        if attrs.get('password') != attrs.pop('password_confirm'):
            raise serializers.ValidationError({"password": "Passwords do not match."})
        
        # If username not provided, derive from email prefix
        if not attrs.get('username'):
            attrs['username'] = attrs['email'].split('@')[0]
        
        # Security: Default public registration to 'student' unless specifically allowed
        if attrs.get('role') == 'admin':
            attrs['role'] = 'student'

        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), source='department', write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'role', 'phone', 'identifier', 'department', 'department_id',
            'avatar', 'created_at'
        ]
        read_only_fields = ['id', 'email', 'role', 'created_at']


class UserListSerializer(serializers.ModelSerializer):
    department_name = serializers.ReadOnlyField(source='department.name')
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name', 'full_name',
            'role', 'phone', 'identifier', 'department', 'department_name', 'is_active', 'created_at'
        ]

    def get_full_name(self, obj):
        return obj.get_full_name() or obj.username
