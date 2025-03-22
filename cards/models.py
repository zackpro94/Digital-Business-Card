from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image
import uuid
from django.urls import reverse

class Company(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='company_logos/', blank=True)
    address = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Companies"


class Employee(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employees')
    name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    profile_picture = models.ImageField(upload_to='employee_pics/', blank=True)
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class IndividualClient(models.Model):
    name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    profile_picture = models.ImageField(upload_to='individual_pics/', blank=True)
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class BusinessCard(models.Model):
    THEME_CHOICES = [
        ('default', 'Default'),
        ('elegant', 'Elegant'),
        ('modern', 'Modern'),
    ]
    
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, null=True, blank=True, related_name='business_card')
    individual_client = models.OneToOneField(IndividualClient, on_delete=models.CASCADE, null=True, blank=True, related_name='business_card')
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)
    views = models.PositiveIntegerField(default=0)
    shares = models.PositiveIntegerField(default=0)
    last_viewed = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    theme = models.CharField(max_length=20, choices=THEME_CHOICES, default='default')

    def __str__(self):
        if self.employee:
            return f"Card for {self.employee.name}"
        elif self.individual_client:
            return f"Card for {self.individual_client.name}"
        return "Unassigned Card"
    
    def save(self, *args, **kwargs):
        # Generate QR code if it doesn't exist
        if not self.qr_code:
            self.generate_qr_code()
        super().save(*args, **kwargs)
    
    def generate_qr_code(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        url = self.get_absolute_url()
        qr.add_data(url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        
        # Set the filename for the QR code image
        filename = f'qr_{self.uuid}.png'
        self.qr_code.save(filename, File(buffer), save=False)
    
    def get_absolute_url(self):
        return reverse('card_detail', kwargs={'uuid': str(self.uuid)})
    
    def increment_view(self):
        self.views += 1
        self.save()
    
    def increment_share(self):
        self.shares += 1
        self.save()


class ContactRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('contacted', 'Contacted'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    company_name = models.CharField(max_length=100, blank=True)
    message = models.TextField()
    card_type = models.CharField(max_length=20, choices=[('individual', 'Individual'), ('company', 'Company')], default='individual')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Request from {self.name} - {self.get_status_display()}"
    
    class Meta:
        ordering = ['-created_at']
