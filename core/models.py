from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class User(AbstractUser):
    """
    Custom User model that can be either a Student or Teacher
    """
    USER_TYPE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]
    
    # User type field
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='student',
        help_text='Whether the user is a student or teacher'
    )
    
    # Additional fields for both user types
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True,
        null=True,
        help_text='Phone number (optional)'
    )
    
    # Profile picture
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True,
        help_text='Profile picture (optional)'
    )
    
    # Bio/description
    bio = models.TextField(
        max_length=500,
        blank=True,
        help_text='Short bio or description'
    )
    
    # Date of birth
    date_of_birth = models.DateField(
        blank=True,
        null=True,
        help_text='Date of birth (optional)'
    )
    
    # Address
    address = models.TextField(
        max_length=200,
        blank=True,
        help_text='Address (optional)'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_user_type_display()})"
    
    @property
    def is_student(self):
        return self.user_type == 'student'
    
    @property
    def is_teacher(self):
        return self.user_type == 'teacher'
    
    def get_full_name_or_username(self):
        """Return full name if available, otherwise username"""
        full_name = self.get_full_name()
        return full_name if full_name else self.username
