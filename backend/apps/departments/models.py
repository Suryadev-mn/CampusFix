import uuid
import io
import qrcode
from django.db import models
from django.core.files.base import ContentFile

class Department(models.Model):
    CATEGORY_CHOICES = (
        ('academic', 'Academic Branch'),
        ('facility', 'Facility / Maintenance'),
    )

    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='facility')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        ordering = ['name']


class Building(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    total_floors = models.PositiveIntegerField(default=1)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        ordering = ['name']


class Classroom(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='classrooms')
    room_number = models.CharField(max_length=50)
    floor = models.PositiveIntegerField(default=0)
    qr_code_token = models.CharField(max_length=64, unique=True, blank=True)
    qr_code_image = models.ImageField(upload_to='qrcodes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('building', 'room_number')
        ordering = ['building', 'room_number']

    def __str__(self):
        return f"{self.building.code} - {self.room_number}"

    def save(self, *args, **kwargs):
        if not self.qr_code_token:
            self.qr_code_token = f"CF-{self.building.code}-{self.room_number}-{uuid.uuid4().hex[:6]}".upper().replace(" ", "")

        # Generate QR code image if not present
        if not self.qr_code_image:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            # The QR code data can be a direct web URL or JSON/token
            qr_data = f"CAMPUSFIX_QR:{self.qr_code_token}"
            qr.add_data(qr_data)
            qr.make(fit=True)

            img = qr.make_image(fill_color="#2563EB", back_color="white")
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            file_name = f"qr_{self.qr_code_token}.png"
            self.qr_code_image.save(file_name, ContentFile(buffer.getvalue()), save=False)

        super().save(*args, **kwargs)
