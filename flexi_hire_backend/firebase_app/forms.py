# firebase_app/forms.py
from django import forms

class JobForm(forms.Form):
    category = forms.CharField(max_length=50, label="Category")
    title = forms.CharField(max_length=100, label="Title")
    specs = forms.CharField(widget=forms.Textarea, help_text="Enter specs separated by commas (e.g., 'SEO knowledge, 10 hrs/week, ₹30k/month')")
    apply_link = forms.URLField(max_length=200, label="Apply Link")