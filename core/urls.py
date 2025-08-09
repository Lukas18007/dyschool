from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sign-in/', views.sign_in, name='sign_in'),
    path('sign-up/', views.sign_up, name='sign_up'),
    path('sign-out/', views.sign_out, name='sign_out'),
    
    # Teacher views
    path('teacher/profile/', views.teacher_profile, name='teacher_profile'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/availability/<int:lesson_request_id>/', views.submit_availability, name='submit_availability'),
    
    # Student views
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('lesson/search/', views.lesson_search, name='lesson_search'),
    path('lesson/request/<int:teacher_id>/', views.lesson_request, name='lesson_request'),
    path('lesson/accept/<int:availability_id>/', views.accept_availability, name='accept_availability'),
    
    # AJAX views
    path('ajax/lesson-topics/', views.get_lesson_topics, name='get_lesson_topics'),
] 