# firebase_app/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.conf import settings

from .forms import JobForm
import firebase_admin
from firebase_admin import credentials, firestore
import datetime


FIREBASE_CREDENTIALS = settings.FIREBASE_CREDENTIALS

# Initialize Firebase Admin SDK
if not firebase_admin._apps:  # Check if already initialized
    cred = credentials.Certificate(FIREBASE_CREDENTIALS)
    firebase_admin.initialize_app(cred)
db = firestore.client()

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! Please log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'firebase_app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome, {username}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'firebase_app/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')

@login_required
def home_view(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            # Save job to Firestore
            job_data = {
                'user': request.user.username,
                'user_id': request.user.id,
                'category': form.cleaned_data['category'],
                'title': form.cleaned_data['title'],
                'specs': form.cleaned_data['specs'],
                'apply_link': form.cleaned_data['apply_link'],
                'created_at': datetime.datetime.now(datetime.timezone.utc),
            }
            db.collection('jobs').add(job_data)
            messages.success(request, 'Job posted successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Error posting job. Please check the form.')
    else:
        form = JobForm()
    
    # Fetch all jobs from Firestore
    jobs = []
    for doc in db.collection('jobs').stream():
        job = doc.to_dict()
        job['id'] = doc.id
        job['specs_list'] = [spec.strip() for spec in job['specs'].split(',')]  # Preprocess specs
        job['created_at'] = job['created_at'].strftime('%B %d, %Y')  # Format timestamp
        jobs.append(job)
    
    return render(request, 'firebase_app/home.html', {'form': form, 'jobs': jobs, 'user': request.user})