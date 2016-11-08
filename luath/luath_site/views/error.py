from django.shortcuts import render

def not_found(request):
    return render(request, 'luath_site/errors/404.html')
