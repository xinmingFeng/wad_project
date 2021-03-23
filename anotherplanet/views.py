from django.shortcuts import render
from django.http import HttpResponse
from anotherplanet.forms import UserForm,UserProfileForm
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.urls import reverse
from django.shortcuts import redirect


# Create your views here.


def categories(request):

    context_dict = {'boldmessage':"find your favorite pet!"}

    return render(request, 'anotherplanet/index.html', context=context_dict)
    return HttpResponse("Categories <a href='/anotherplanet/cat'>CAT</a><br />"
                        "<a href='/anotherplanet/dog'>DOG</a><br />"
                        "<a href='/anotherplanet/smallpets'>SMALLPETS</a><br />"
                        "<a href='/anotherplanet/fish'>FISH</a><br />"
                        )
   


def cat(request):
    return render(request,'anotherplanet/cat.html')
    return HttpResponse("Cat <a href='/anotherplanet/'>Categories</a>")

def dog(request):

    return render(request,'anotherplanet/dog.html')
    return HttpResponse("Dog <a href='/anotherplanet/'>Categories</a>")

def smallpets(request):

    return render(request,'anotherplanet/smallpets.html')
    return HttpResponse("Smallpets <a href='/anotherplanet/'>Categories</a>")

def fish(request):
    return render(request,'anotherplanet/fish.html')
    return HttpResponse("fish <a href='/anotherplanet/'>Categories</a>")

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                  'anotherplanet/register.html',
                  context = {'user_form':user_form,
                             'profile_form':profile_form,
                             'registered':registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('anotherplanet:index'))
            else:
                return HttpPesponse("Your anotherplanet account is disabled.")
        else:
            print(f"Invalid login login details: {username},{password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'anotherplanet/login.html')


@login_required
def restricted(request):
    return render(request, 'anotherplanet/restricted.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('anotherplanet:index'))