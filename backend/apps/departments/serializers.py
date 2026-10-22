from rest_framework import serializers
from .models import Department, Building, Classroom

class DepartmentSerializer(serializers.ModelSerializer):
    issue_count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Department
        fields = ['id', 'name', 'code', 'category', 'description', 'created_at', 'issue_count']


class ClassroomSerializer(serializers.ModelSerializer):
    building_name = serializers.ReadOnlyField(source='building.name')
    building_code = serializers.ReadOnlyField(source='building.code')

    class Meta:
        model = Classroom
        fields = ['id', 'building', 'building_name', 'building_code', 'room_number', 'floor', 'qr_code_token', 'qr_code_image', 'created_at']


class BuildingSerializer(serializers.ModelSerializer):
    classrooms = ClassroomSerializer(many=True, read_only=True)
    total_classrooms = serializers.IntegerField(source='classrooms.count', read_only=True)

    class Meta:
        model = Building
        fields = ['id', 'name', 'code', 'total_floors', 'description', 'created_at', 'classrooms', 'total_classrooms']
