from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, "resume_reviewer/base.html")
