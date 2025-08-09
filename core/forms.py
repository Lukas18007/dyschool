from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, TeacherProfile, LessonRequest, TeacherAvailability, Specialization, LessonTopic

class UserRegistrationForm(UserCreationForm):
    """Custom user registration form"""
    
    # Override email field to make it required
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your email'
        })
    )
    
    # Override first_name and last_name to make them required
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your first name'
        })
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your last name'
        })
    )
    
    # Override username field
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Choose a username'
        })
    )
    
    # Override password fields
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Create a password'
        })
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Confirm your password'
        })
    )
    
    # User type field
    user_type = forms.ChoiceField(
        choices=User.USER_TYPE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    # Phone number field
    phone_number = forms.CharField(
        max_length=17,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Phone number (optional)'
        })
    )
    
    # Bio field
    bio = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-textarea',
            'placeholder': 'Tell us about yourself (optional)',
            'rows': 3
        })
    )
    
    # Date of birth field
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-input',
            'type': 'date'
        })
    )
    
    # Address field
    address = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-textarea',
            'placeholder': 'Your address (optional)',
            'rows': 2
        })
    )
    
    # Profile picture field
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-file'
        })
    )
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 'password1', 'password2',
            'user_type', 'phone_number', 'bio', 'date_of_birth', 'address', 'profile_picture'
        ]
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.user_type = self.cleaned_data['user_type']
        user.phone_number = self.cleaned_data.get('phone_number', '')
        user.bio = self.cleaned_data.get('bio', '')
        user.date_of_birth = self.cleaned_data.get('date_of_birth')
        user.address = self.cleaned_data.get('address', '')
        
        if self.cleaned_data.get('profile_picture'):
            user.profile_picture = self.cleaned_data['profile_picture']
        
        if commit:
            user.save()
        return user


class TeacherProfileForm(forms.ModelForm):
    """Form for creating/editing teacher profile"""
    
    class Meta:
        model = TeacherProfile
        fields = ['specializations', 'lesson_topics', 'hourly_rate', 'experience_years', 'about']
        widgets = {
            'specializations': forms.CheckboxSelectMultiple(attrs={'class': 'form-checkbox'}),
            'lesson_topics': forms.CheckboxSelectMultiple(attrs={'class': 'form-checkbox'}),
            'hourly_rate': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter your hourly rate',
                'min': '0',
                'step': '0.01'
            }),
            'experience_years': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Years of teaching experience',
                'min': '0'
            }),
            'about': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Tell us about your teaching experience and approach...',
                'rows': 5
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter lesson topics based on selected specializations
        if self.instance.pk:
            self.fields['lesson_topics'].queryset = LessonTopic.objects.filter(
                specialization__in=self.instance.specializations.all()
            )


class LessonRequestForm(forms.ModelForm):
    """Form for creating lesson requests"""
    
    class Meta:
        model = LessonRequest
        fields = ['lesson_topic', 'lesson_duration', 'max_hourly_rate', 'additional_notes']
        widgets = {
            'lesson_topic': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Select lesson topic'
            }),
            'lesson_duration': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Duration in minutes',
                'min': '30',
                'max': '180'
            }),
            'max_hourly_rate': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Maximum hourly rate you can pay',
                'min': '0',
                'step': '0.01'
            }),
            'additional_notes': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Any additional notes or requirements...',
                'rows': 3
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show lesson topics that have teachers available
        self.fields['lesson_topic'].queryset = LessonTopic.objects.filter(
            teachers__isnull=False
        ).distinct()


class TeacherAvailabilityForm(forms.ModelForm):
    """Form for teachers to submit their availability"""
    
    class Meta:
        model = TeacherAvailability
        fields = ['available_date', 'available_time', 'duration']
        widgets = {
            'available_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date',
                'min': 'today'
            }),
            'available_time': forms.TimeInput(attrs={
                'class': 'form-input',
                'type': 'time'
            }),
            'duration': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Duration in minutes',
                'min': '30',
                'max': '180'
            })
        }
    
    def clean_available_date(self):
        from datetime import date
        available_date = self.cleaned_data.get('available_date')
        if available_date and available_date < date.today():
            raise forms.ValidationError("Available date cannot be in the past.")
        return available_date


class LessonSearchForm(forms.Form):
    """Form for students to search for lessons"""
    specialization = forms.ModelChoiceField(
        queryset=Specialization.objects.all(),
        empty_label="Select specialization",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    lesson_topic = forms.ModelChoiceField(
        queryset=LessonTopic.objects.none(),
        empty_label="Select lesson topic",
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    max_hourly_rate = forms.DecimalField(
        max_digits=8,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-input',
            'placeholder': 'Maximum hourly rate',
            'min': '0',
            'step': '0.01'
        })
    )
    lesson_duration = forms.IntegerField(
        min_value=30,
        max_value=180,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-input',
            'placeholder': 'Duration in minutes',
            'min': '30',
            'max': '180'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Update lesson topics based on selected specialization
        if 'specialization' in self.data:
            try:
                specialization_id = int(self.data.get('specialization'))
                self.fields['lesson_topic'].queryset = LessonTopic.objects.filter(
                    specialization_id=specialization_id
                )
            except (ValueError, TypeError):
                pass 