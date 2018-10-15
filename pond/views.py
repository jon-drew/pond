from django.http import HttpResponse
from django.shortcuts import render, redirect

def RedirectView(request):
    return redirect('/login/')