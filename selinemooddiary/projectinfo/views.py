from django.shortcuts import render

def index(request):
    return render(request, 'projectinfo/aboutproject.html', {'usr': request.user})
