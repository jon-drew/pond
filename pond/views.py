from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import ContactForm, LoginForm, RegisterForm

def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        'form': form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        username  = form.cleaned_data.get('username')
        password  = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('/')
        else:
            print('Error')
    return render(request, 'accounts/login.html', context)

def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        'form': form
    }
    if form.is_valid():
        username  = form.cleaned_data.get('username')
        password  = form.cleaned_data.get('password')
        new_user  = User.objects.create_user(username, password)

    return render(request, 'accounts/register.html', context)

def home_page(request):
    context = {
        'title':'hello world',
        'content':'Welocome to pond',
    }
    if request.user.is_authenticated:
        context = {
            'title':'hello world',
            'content':'Jump In',
            'custom_welcome': 'Hello ', # + str(User),
        }

    return render(request, 'home_page.html', context)

def about_page(request):
    context = {
        'title':'About Page',
        'content':'Pond is an invitation sharing platform.'
    }

    return render(request, 'home_page.html', context)

def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        "title":"Contact",
        "content":" Welcome to the contact page.",
        "form": contact_form,
    }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
        if request.is_ajax():
            return JsonResponse({"message": "We will respond to your message soon."})

    if contact_form.errors:
        errors = contact_form.errors.as_json()
        if request.is_ajax():
            return HttpResponse(errors, status=400, content_type='application/json')

    return render(request, "contact/view.html", context)
