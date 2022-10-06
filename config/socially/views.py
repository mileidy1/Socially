
from django.shortcuts import render
from .models import *

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