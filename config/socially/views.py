from django.urls import reverse, reverse
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.http import HttpResponseRedirect

def index(request, args):
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
    post = get_object_or_404(Socially, id=request.POST.get('like'))
    post.like.add(request.user)
    return HttpResponseRedirect(reverse('socially:index', args=[str(pk)]))
