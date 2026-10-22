from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from .models import Department, Building, Classroom
from .serializers import DepartmentSerializer, BuildingSerializer, ClassroomSerializer

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'admin'


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.annotate(issue_count=Count('issues')).all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category') or self.request.query_params.get('type')
        if category:
            queryset = queryset.filter(category=category)
        return queryset


class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.prefetch_related('classrooms').all()
    serializer_class = BuildingSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None


class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.select_related('building').all()
    serializer_class = ClassroomSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None

    def get_queryset(self):
        queryset = super().get_queryset()
        building_id = self.request.query_params.get('building')
        if building_id:
            queryset = queryset.filter(building_id=building_id)
        return queryset


class QRCodeLookupView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, token):
        # Support raw token or CAMPUSFIX_QR: prefix
        clean_token = token.replace('CAMPUSFIX_QR:', '').strip().upper()
        
        classroom = Classroom.objects.select_related('building').filter(
            qr_code_token__iexact=clean_token
        ).first()

        if not classroom:
            classroom = Classroom.objects.select_related('building').filter(
                qr_code_token__istartswith=clean_token
            ).first()

        if not classroom:
            # Try searching by room number or building
            classroom = Classroom.objects.select_related('building').filter(
                qr_code_token__icontains=clean_token
            ).first()

        if classroom:
            return Response({
                'found': True,
                'classroom': ClassroomSerializer(classroom).data,
                'building': {
                    'id': classroom.building.id,
                    'name': classroom.building.name,
                    'code': classroom.building.code
                }
            })

        return Response(
            {'found': False, 'error': 'Invalid QR Code or Classroom not found.'},
            status=status.HTTP_404_NOT_FOUND
        )
