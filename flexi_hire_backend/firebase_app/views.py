# flexi_hire_backend/flexi_hire_backend/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .forms import JobForm
import firebase_admin
from firebase_admin import credentials, firestore
import datetime

# Hardcoded Firebase credentials
FIREBASE_CREDENTIALS = {
  "type": "service_account",
  "project_id": "flexi-hire",
  "private_key_id": "c52f9edc9d7433839d881bb8d8ec0cdef329da98",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCBdHBknh9Fql2h\nZKrXN5xNeseaxXy+KA1yo7nel/Cc/C084rjJP0hYiRrXkXsER8b49JmTRiFNbPQt\nIOTXGu2eruQBaaFe/UhIUnb+6WtrEdPG3tiPvLPo/dDWhsXZJfuBY/Kcp2AQeloE\nLu3qR6RXyyNpvm5T2/GxwVNQ1glEct2PPzU9BjR5vOfKvkROm6VvzER3Whpe/BFv\nQPlx6h8HsJn9WilBsn9JbEwCRjUi1QvpurLduBzo0If5gxRGq5nfj5PL+D6xnyFd\nW/o2Wf3eZ3xjXEiAg0VGKB9G0B8M7YUITeJPAEwGO4bF2kPbxT3SPYMbz1jVRWoA\nxeij2SNhAgMBAAECggEAC8ly0a6AsW1S1iGeLoyz2213pCohcrJJ5dYY0+F+DoUl\nh1ArZrjaLk7ZgKbl47IMtgPrbHiWYAAwzApyhlAU3P3BPoxZcuvZO4CKsNNxrOTe\nz/zgDK0FV+GttK1pG/L0j0eZl6rjuSGyytkNCj0DWTJiozusEaWf6uvr2UXhFSLG\neUQ4HnptbF9vIVfNHJytDVH1PpRAwH7bfZobAiK89aee7vchp3P15kvW2v76zBnp\nCupnqJvZ645UTqjoTzQv4t9USOCh6AY+fnRRU9DnonCqpIUQizM20E/aihUdRgPT\nbGmzrkyoZHfQH/tf/0oFA43Yr0jaC/B1EhKdI8YLmwKBgQC2SMFfxEC0FExCgKgY\nOFcL5iRAsiINGrxwCsjEhOgr/8he/12JWu6aDadli9T8GbJDywGXBK+CXxyt5v1J\nOTA2MklWbhghNWEM7Xjsbw6x/PrvONt3Ni1YECBwyMz3TggAqY7ZyXw9Nf8r38j6\nM6GIToC2brgoFKGpcMhCJkwZwwKBgQC1znHvAtcyCcezHtD5YZctj+e6TNLGo+Kt\njLMn3cRcOP9LFz0ZsBUZkcE7mbiyw9kp8Ve/eSfXgTutLwHSkeeRkIVrbUQtgJVZ\nA32ATibnYFXCk9Tk/C38Gpgxvqh/FI8uOmOXjgu9XebbDdgk1x98C4MhNwY3QtLq\nLPHoXtNYCwKBgQCp21/+KjUU2Pk62wJIF2/dkaXkd1lNlsVTLmlo3mQuY9nF0/XI\nQWinOuPqtwNPq242x9uCawZU2OYzklQhQF4RkohONqbbgw8dacfNoasy5ga6lePD\n0UMtlVF1Z1e/dwH0BAwuGxdfPoq5yn1P0H7MMkK0PLXz+02tQ4AITAGL2wKBgD+7\ndRkyR7nUz9qszNj/Kv3f2n3mfGUCAm6QSiWJilJB8MykAtlEbsEd5T09cA/KtBAN\n+JK4qAzV0tOtDNiCKUlP/lVgYmwJDVG89XvK6bxmeunQ5Oq4tG4R7JRTn8GctWyh\nL1RriRYDGvBjdAfGGdVkO72jClzI4iMRSmQJCdFtAoGAUM8MshDitfkmxZBtdq/r\nrYNpUf0FZHRqhNzaWf1CqsBTDgYvRnNIBhHmgWM+Ft1ewwRbc0PGLD3J41urd89V\nPvFLwNdQTmPsdGVgwnUeNvsKAVEqmiU2qMgU/xwZEjp+xWk2xiAL/xcDnrHB/HUf\nKaeoYHQkt2hMEfdqX9tPsZ4=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-fbsvc@flexi-hire.iam.gserviceaccount.com",
  "client_id": "104501187203109446759",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40flexi-hire.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

# Initialize Firebase Admin SDK with error handling
try:
    if not firebase_admin._apps:
        cred = credentials.Certificate(FIREBASE_CREDENTIALS)
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
    return render(request, 'ffirebase_app/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')

@login_required
def home_view(request):
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
    else:
        form = JobForm()
    
    # Fetch all jobs from Firestore
    try:
        jobs = []
        for doc in db.collection('jobs').stream():
            job = doc.to_dict()
            job['id'] = doc.id
            job['specs_list'] = [spec.strip() for spec in job['specs'].split(',')]
            job['created_at'] = job['created_at'].strftime('%B %d, %Y')
            jobs.append(job)
    except Exception as e:
        messages.error(request, f'Error fetching jobs from Firestore: {str(e)}')
        jobs = []
    
    return render(request, 'firebase_app/home.html', {'form': form, 'jobs': jobs, 'user': request.user})