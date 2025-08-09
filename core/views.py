from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.db.models import Q
from .forms import (
    UserRegistrationForm, TeacherProfileForm, LessonRequestForm, 
    TeacherAvailabilityForm, LessonSearchForm
)
from .models import (
    User, TeacherProfile, LessonRequest, TeacherAvailability, 
    LessonBooking, Specialization, LessonTopic
)

def sign_in(request):
    """Sign in view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_full_name_or_username()}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'core/sign_in.html', {'form': form})

def sign_up(request):
    """Sign up view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to Dyschool, {user.get_full_name_or_username()}!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'core/sign_up.html', {'form': form})

@login_required
def sign_out(request):
    """Sign out view"""
    logout(request)
    messages.info(request, 'You have been successfully signed out.')
    return redirect('sign_in')

def home(request):
    """Home page view"""
    return render(request, 'core/home.html')

@login_required
def teacher_profile(request):
    """Teacher profile creation/editing view"""
    if not request.user.is_teacher:
        messages.error(request, 'Only teachers can access this page.')
        return redirect('home')
    
    try:
        teacher_profile = request.user.teacher_profile
    except TeacherProfile.DoesNotExist:
        teacher_profile = None
    
    if request.method == 'POST':
        form = TeacherProfileForm(request.POST, instance=teacher_profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            form.save_m2m()  # Save many-to-many relationships
            messages.success(request, 'Teacher profile updated successfully!')
            return redirect('teacher_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TeacherProfileForm(instance=teacher_profile)
    
    return render(request, 'core/teacher_profile.html', {'form': form})

@login_required
def lesson_search(request):
    """Lesson search view for students"""
    if not request.user.is_student:
        messages.error(request, 'Only students can search for lessons.')
        return redirect('home')
    
    form = LessonSearchForm(request.GET or None)
    teachers = []
    
    if form.is_valid():
        specialization = form.cleaned_data.get('specialization')
        lesson_topic = form.cleaned_data.get('lesson_topic')
        max_hourly_rate = form.cleaned_data.get('max_hourly_rate')
        lesson_duration = form.cleaned_data.get('lesson_duration')
        
        # Build query for teachers
        teacher_profiles = TeacherProfile.objects.filter(is_available=True)
        
        if specialization:
            teacher_profiles = teacher_profiles.filter(specializations=specialization)
        
        if lesson_topic:
            teacher_profiles = teacher_profiles.filter(lesson_topics=lesson_topic)
        
        if max_hourly_rate:
            teacher_profiles = teacher_profiles.filter(hourly_rate__lte=max_hourly_rate)
        
        teachers = [profile.user for profile in teacher_profiles]
    
    return render(request, 'core/lesson_search.html', {
        'form': form,
        'teachers': teachers
    })

@login_required
def lesson_request(request, teacher_id):
    """Create a lesson request for a specific teacher"""
    if not request.user.is_student:
        messages.error(request, 'Only students can create lesson requests.')
        return redirect('home')
    
    teacher = get_object_or_404(User, id=teacher_id, user_type='teacher')
    
    if request.method == 'POST':
        form = LessonRequestForm(request.POST)
        if form.is_valid():
            lesson_request = form.save(commit=False)
            lesson_request.student = request.user
            lesson_request.save()
            messages.success(request, f'Lesson request sent to {teacher.get_full_name()}!')
            return redirect('student_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LessonRequestForm()
    
    return render(request, 'core/lesson_request.html', {
        'form': form,
        'teacher': teacher
    })

@login_required
def teacher_dashboard(request):
    """Dashboard for teachers"""
    if not request.user.is_teacher:
        messages.error(request, 'Only teachers can access this page.')
        return redirect('home')
    
    try:
        teacher_profile = request.user.teacher_profile
    except TeacherProfile.DoesNotExist:
        return redirect('teacher_profile')
    
    # Get lesson requests that match teacher's specializations
    lesson_requests = LessonRequest.objects.filter(
        lesson_topic__in=teacher_profile.lesson_topics.all(),
        status='pending'
    ).exclude(
        student=request.user
    ).order_by('-created_at')
    
    # Get teacher's availabilities
    availabilities = TeacherAvailability.objects.filter(
        teacher=request.user
    ).order_by('-created_at')
    
    # Get bookings
    bookings = LessonBooking.objects.filter(
        teacher=request.user
    ).order_by('-created_at')
    
    return render(request, 'core/teacher_dashboard.html', {
        'teacher_profile': teacher_profile,
        'lesson_requests': lesson_requests,
        'availabilities': availabilities,
        'bookings': bookings
    })

@login_required
def student_dashboard(request):
    """Dashboard for students"""
    if not request.user.is_student:
        messages.error(request, 'Only students can access this page.')
        return redirect('home')
    
    # Get student's lesson requests
    lesson_requests = LessonRequest.objects.filter(
        student=request.user
    ).order_by('-created_at')
    
    # Get availabilities for student's requests
    availabilities = TeacherAvailability.objects.filter(
        lesson_request__student=request.user
    ).order_by('-created_at')
    
    return render(request, 'core/student_dashboard.html', {
        'lesson_requests': lesson_requests,
        'availabilities': availabilities
    })

@login_required
def submit_availability(request, lesson_request_id):
    """Submit availability for a lesson request"""
    if not request.user.is_teacher:
        messages.error(request, 'Only teachers can submit availability.')
        return redirect('home')
    
    lesson_request = get_object_or_404(LessonRequest, id=lesson_request_id)
    
    if request.method == 'POST':
        form = TeacherAvailabilityForm(request.POST)
        if form.is_valid():
            availability = form.save(commit=False)
            availability.teacher = request.user
            availability.lesson_request = lesson_request
            availability.save()
            messages.success(request, 'Availability submitted successfully!')
            return redirect('teacher_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TeacherAvailabilityForm()
    
    return render(request, 'core/submit_availability.html', {
        'form': form,
        'lesson_request': lesson_request
    })

@login_required
def accept_availability(request, availability_id):
    """Accept a teacher's availability"""
    if not request.user.is_student:
        messages.error(request, 'Only students can accept availability.')
        return redirect('home')
    
    availability = get_object_or_404(TeacherAvailability, id=availability_id)
    
    # Check if the student owns the lesson request
    if availability.lesson_request.student != request.user:
        messages.error(request, 'You can only accept availability for your own lesson requests.')
        return redirect('student_dashboard')
    
    # Create booking
    booking = LessonBooking.objects.create(
        lesson_request=availability.lesson_request,
        teacher=availability.teacher,
        teacher_availability=availability
    )
    
    # Mark availability as accepted
    availability.is_accepted = True
    availability.save()
    
    # Update lesson request status
    lesson_request = availability.lesson_request
    lesson_request.status = 'matched'
    lesson_request.save()
    
    messages.success(request, f'Lesson booked with {availability.teacher.get_full_name()}!')
    return redirect('student_dashboard')

def get_lesson_topics(request):
    """AJAX view to get lesson topics for a specialization"""
    specialization_id = request.GET.get('specialization_id')
    if specialization_id:
        lesson_topics = LessonTopic.objects.filter(specialization_id=specialization_id)
        data = [{'id': topic.id, 'name': topic.name} for topic in lesson_topics]
        return JsonResponse({'lesson_topics': data})
    return JsonResponse({'lesson_topics': []})
