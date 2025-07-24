# flexi_hire_backend/flexi_hire_backend/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .forms import JobForm
import firebase_admin
from firebase_admin import credentials, firestore
import datetime
from django.conf import settings
import os

# Initialize Firebase Admin SDK with error handling
try:
    if not firebase_admin._apps:
        if not os.path.exists(settings.FIREBASE_CREDENTIALS):
            raise FileNotFoundError(f"Firebase credentials file not found at: {settings.FIREBASE_CREDENTIALS}")
        cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS)
        firebase_admin.initialize_app(cred)
    db = firestore.client()
except Exception as e:
    raise Exception(f"Failed to initialize Firebase: {str(e)}")

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
    search_query = request.GET.get('search', '')  # Get search query from URL
    form = JobForm()

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            try:
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
            except Exception as e:
                messages.error(request, f'Error posting job to Firestore: {str(e)}')
        else:
            messages.error(request, 'Error posting job. Please check the form.')

    # Fetch jobs from Firestore with optional search
    try:
        jobs = []
        query = db.collection('jobs')
        for doc in query.stream():
            job = doc.to_dict()
            job['id'] = doc.id
            specs = job.get('specs', '')
            job['specs_list'] = [spec.strip() for spec in specs.split(',')] if specs and isinstance(specs, str) else []
            job['created_at'] = job.get('created_at', datetime.datetime.now(datetime.timezone.utc)).strftime('%B %d, %Y')
            # Filter jobs by search query (case-insensitive)
            if search_query.lower() in job.get('title', '').lower() or search_query.lower() in job.get('category', '').lower():
                jobs.append(job)
    except Exception as e:
        messages.error(request, f'Error fetching jobs from Firestore: {str(e)}')
        jobs = []

    return render(request, 'firebase_app/home.html', {
        'form': form,
        'jobs': jobs,
        'user': request.user,
        'search_query': search_query
    })

@login_required
def delete_job_view(request, job_id):
    try:
        job_ref = db.collection('jobs').document(job_id)
        job = job_ref.get()
        if not job.exists:
            messages.error(request, 'Job not found.')
            return redirect('home')
        job_data = job.to_dict()
        if job_data.get('user_id') != request.user.id:
            messages.error(request, 'You are not authorized to delete this job.')
            return redirect('home')
        job_ref.delete()
        messages.success(request, 'Job deleted successfully!')
    except Exception as e:
        messages.error(request, f'Error deleting job: {str(e)}')
    return redirect('home')

@login_required
def edit_job_view(request, job_id):
    try:
        job_ref = db.collection('jobs').document(job_id)
        job = job_ref.get()
        if not job.exists:
            messages.error(request, 'Job not found.')
            return redirect('home')
        job_data = job.to_dict()
        if job_data.get('user_id') != request.user.id:
            messages.error(request, 'You are not authorized to edit this job.')
            return redirect('home')

        if request.method == 'POST':
            form = JobForm(request.POST)
            if form.is_valid():
                try:
                    updated_data = {
                        'user': request.user.username,
                        'user_id': request.user.id,
                        'category': form.cleaned_data['category'],
                        'title': form.cleaned_data['title'],
                        'specs': form.cleaned_data['specs'],
                        'apply_link': form.cleaned_data['apply_link'],
                        'created_at': job_data.get('created_at', datetime.datetime.now(datetime.timezone.utc)),
                    }
                    job_ref.set(updated_data)
                    messages.success(request, 'Job updated successfully!')
                    return redirect('home')
                except Exception as e:
                    messages.error(request, f'Error updating job: {str(e)}')
            else:
                messages.error(request, 'Error updating job. Please check the form.')
        else:
            # Pre-fill form with existing job data
            form = JobForm(initial={
                'category': job_data.get('category', ''),
                'title': job_data.get('title', ''),
                'specs': job_data.get('specs', ''),
                'apply_link': job_data.get('apply_link', ''),
            })
    except Exception as e:
        messages.error(request, f'Error fetching job: {str(e)}')
        return redirect('home')

    return render(request, 'firebase_app/edit_job.html', {'form': form, 'job_id': job_id})

# Checking commit status