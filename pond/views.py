from django.http import HttpResponse
from django.shortcuts import render, redirect

def RedirectView(request):
    if request.user.is_authenticated:
        return redirect('ribbits:list')
    return redirect('/login/')
