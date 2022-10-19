from .models import *
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from .models import Profile, LikePost, FollowersCount
from itertools import chain
import random


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

def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Socially.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.number_of_likes = post.number_of_likes+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.number_of_likes = post.number_of_likes-1
        post.save()
        return redirect('/')

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
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        
        return redirect('settings')
    return render(request, 'setting.html', {'user_profile': user_profile})