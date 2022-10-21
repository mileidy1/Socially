from django.urls import reverse, reverse
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, auth
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile,  FollowersCount
from itertools import chain
import random
from django.contrib import messages
def index(request):
    context = {}
    if request.method == 'POST':
        if request.user.is_authenticated:
            social_text = request.POST.get('social-text')
            socially_user = request.user
            Socially.objects.create(social_text=social_text, author=socially_user)
        else:
            context['message'] = 'You are not logged in.'
    all_socials = Socially.objects.all()
    def get_context_data(self, *args, **kwargs):
        stuff=get_object_or_404(Socially, id=self.kwargs['pk'])
        total_like = stuff.total_like()
        context["total_like"] = total_like
        return context
    context['all_socials']= all_socials
    return render(request, 'socially/index.html', context)

def user_socials(request, this_user):
    context = {}
    if request.method == 'POST':
        if request.user.is_authenticated:
            social_text = request.POST.get('social-text')
            socially_user = request.user
            Socially.objects.create(social_text=social_text, author=socially_user)
        else:
            context['message'] = 'You are not logged in.'
    this_user = User.objects.get(username=this_user)
    all_socials = Socially.objects.filter(author=this_user)
    context['all_ socials']= all_socials
    return render(request, 'socially/index.html', context)

def delete(request, id):
    social = Socially.objects.get(id = id)
    social.delete()
    return redirect('/socially/index/')

def likes(request, pk):
    print(pk)
    post = get_object_or_404(Socially, id=pk)
    print(post)
    post.like.add(request.user)
    return HttpResponseRedirect(reverse('socially:index'))

@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
        
        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})
@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Socially.objects.filter(user=pk)
    user_post_length = len(user_posts)

    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
    }
    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')

@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        
        if request.FILES.get('image') == None:
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('image') != None:
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        
        return redirect('settings')
    return render(request, 'setting.html', {'user_profile': user_profile})

def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                #create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
        
    else:
        return render(request, 'signup.html')

def signin(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')

    else:
        return render(request, 'signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')