# # auth_app/models.py
# from django.db import models
# from django.contrib.auth.models import User

# class Job(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to authenticated user
#     category = models.CharField(max_length=50)
#     title = models.CharField(max_length=100)
#     specs = models.TextField()  # Store specs as a single text field (comma-separated or JSON)
#     apply_link = models.URLField(max_length=200)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.title