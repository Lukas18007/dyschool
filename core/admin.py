from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User, Specialization, LessonTopic, TeacherProfile, 
    LessonRequest, TeacherAvailability, LessonBooking
)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Custom admin for User model"""
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_active', 'date_joined')
    list_filter = ('user_type', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('user_type', 'phone_number', 'profile_picture', 'bio', 'date_of_birth', 'address')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('user_type', 'phone_number', 'profile_picture', 'bio', 'date_of_birth', 'address')
        }),
    )


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    """Admin for Specialization model"""
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)
    list_per_page = 20


@admin.register(LessonTopic)
class LessonTopicAdmin(admin.ModelAdmin):
    """Admin for LessonTopic model"""
    list_display = ('name', 'specialization', 'description', 'created_at')
    list_filter = ('specialization', 'created_at')
    search_fields = ('name', 'description', 'specialization__name')
    ordering = ('specialization', 'name')
    list_per_page = 20


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    """Admin for TeacherProfile model"""
    list_display = ('user', 'hourly_rate', 'experience_years', 'is_available', 'created_at')
    list_filter = ('is_available', 'experience_years', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'about')
    ordering = ('-created_at',)
    list_per_page = 20
    
    filter_horizontal = ('specializations', 'lesson_topics')


@admin.register(LessonRequest)
class LessonRequestAdmin(admin.ModelAdmin):
    """Admin for LessonRequest model"""
    list_display = ('student', 'lesson_topic', 'lesson_duration', 'max_hourly_rate', 'status', 'created_at')
    list_filter = ('status', 'lesson_topic__specialization', 'created_at')
    search_fields = ('student__username', 'student__first_name', 'student__last_name', 'lesson_topic__name')
    ordering = ('-created_at',)
    list_per_page = 20


@admin.register(TeacherAvailability)
class TeacherAvailabilityAdmin(admin.ModelAdmin):
    """Admin for TeacherAvailability model"""
    list_display = ('teacher', 'lesson_request', 'available_date', 'available_time', 'duration', 'is_accepted')
    list_filter = ('is_accepted', 'available_date', 'created_at')
    search_fields = ('teacher__username', 'teacher__first_name', 'teacher__last_name')
    ordering = ('available_date', 'available_time')
    list_per_page = 20


@admin.register(LessonBooking)
class LessonBookingAdmin(admin.ModelAdmin):
    """Admin for LessonBooking model"""
    list_display = ('lesson_request', 'teacher', 'teacher_availability', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('lesson_request__student__username', 'teacher__username')
    ordering = ('-created_at',)
    list_per_page = 20
