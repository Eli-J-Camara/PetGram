from django.shortcuts import render

def homepage(request):
    return render(request, 'homepage.html')

def error_404_view(request,):
    return render(request, '404.html', status=404)

def error_500_view(request):
    return render(request, '500.html', status=500)
