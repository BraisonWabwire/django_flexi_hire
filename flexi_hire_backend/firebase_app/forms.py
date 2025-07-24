# firebase_app/forms.py
from django import forms

class JobForm(forms.Form):
    category = forms.CharField(max_length=50, label="Category")
    title = forms.CharField(max_length=100, label="Title")
    specs = forms.CharField(widget=forms.Textarea, help_text="Enter specs separated by commas (e.g., 'SEO knowledge, 10 hrs/week, ₹30k/month')")
    apply_link = forms.URLField(max_length=200, label="Apply Link")

# flexi_hire_backend/flexi_hire_backend/forms.py
class JobForm(forms.Form):
    category = forms.ChoiceField(
        choices=[('', 'Select a category')] + [('Web Development', 'Web Development'), ('Mobile Development', 'Mobile Development'), ('Design', 'Design'), ('Marketing', 'Marketing')],
        widget=forms.Select(attrs={'placeholder': 'e.g., Web Development'}),
        required=True
    )
    title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'e.g., Senior Flutter Developer'}),
        required=True
    )
    specs = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'e.g., SEO knowledge, 10 hrs/week'}),
        required=True
    )
    apply_link = forms.URLField(
        widget=forms.URLInput(attrs={'placeholder': 'e.g., https://apply.example.com'}),
        required=True
    )