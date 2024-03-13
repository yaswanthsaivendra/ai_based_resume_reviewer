from django.urls import path

from resume_reviewer.views import home

urlpatterns = [
    path("", home, name="home"),
]
