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


class Specialization(models.Model):
    """
    Model for music specializations (e.g., Piano, Guitar, Voice, Music Theory)
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Specialization'
        verbose_name_plural = 'Specializations'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class LessonTopic(models.Model):
    """
    Model for specific lesson topics within a specialization
    """
    specialization = models.ForeignKey(
        Specialization,
        on_delete=models.CASCADE,
        related_name='lesson_topics'
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Lesson Topic'
        verbose_name_plural = 'Lesson Topics'
        ordering = ['specialization', 'name']
        unique_together = ['specialization', 'name']
    
    def __str__(self):
        return f"{self.specialization.name} - {self.name}"


class TeacherProfile(models.Model):
    """
    Extended profile for teachers with their specializations and rates
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='teacher_profile'
    )
    specializations = models.ManyToManyField(
        Specialization,
        related_name='teachers'
    )
    lesson_topics = models.ManyToManyField(
        LessonTopic,
        related_name='teachers',
        blank=True
    )
    hourly_rate = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text='Hourly rate in local currency'
    )
    experience_years = models.PositiveIntegerField(
        help_text='Years of teaching experience'
    )
    about = models.TextField(
        help_text='Detailed description of teaching experience and approach'
    )
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Teacher Profile'
        verbose_name_plural = 'Teacher Profiles'
    
    def __str__(self):
        return f"{self.user.get_full_name()} - Teacher Profile"


class LessonRequest(models.Model):
    """
    Model for student lesson requests
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('matched', 'Matched'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='lesson_requests'
    )
    lesson_topic = models.ForeignKey(
        LessonTopic,
        on_delete=models.CASCADE,
        related_name='lesson_requests'
    )
    lesson_duration = models.PositiveIntegerField(
        help_text='Duration in minutes'
    )
    max_hourly_rate = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text='Maximum hourly rate student can pay'
    )
    additional_notes = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Lesson Request'
        verbose_name_plural = 'Lesson Requests'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.student.get_full_name()} - {self.lesson_topic.name}"


class TeacherAvailability(models.Model):
    """
    Model for teacher availability periods
    """
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='availabilities'
    )
    lesson_request = models.ForeignKey(
        LessonRequest,
        on_delete=models.CASCADE,
        related_name='teacher_availabilities'
    )
    available_date = models.DateField()
    available_time = models.TimeField()
    duration = models.PositiveIntegerField(
        help_text='Duration in minutes'
    )
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Teacher Availability'
        verbose_name_plural = 'Teacher Availabilities'
        ordering = ['available_date', 'available_time']
        unique_together = ['teacher', 'lesson_request', 'available_date', 'available_time']
    
    def __str__(self):
        return f"{self.teacher.get_full_name()} - {self.available_date} {self.available_time}"


class LessonBooking(models.Model):
    """
    Model for confirmed lesson bookings
    """
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    lesson_request = models.ForeignKey(
        LessonRequest,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    teacher_availability = models.ForeignKey(
        TeacherAvailability,
        on_delete=models.CASCADE,
        related_name='booking'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='confirmed'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Lesson Booking'
        verbose_name_plural = 'Lesson Bookings'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.lesson_request.student.get_full_name()} with {self.teacher.get_full_name()}"
