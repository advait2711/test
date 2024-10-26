from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),         # Home page URL
    path('resume/', views.gen_resume, name='resume'),  # Resume generation URL
    path('upload/', views.upload_file, name='upload_file'),  # File upload URL
]
