from django.urls import path
from . import views

app_name = 'socially'
urlpatterns = [
    path('index', views.index, name='index'),
    path('<str:this_user>', views.user_socials, name='user_socials'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('like/<int:pk>', views.likes, name='likes'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout, name='logout'),
    path('follow', views.follow, name='follow'),
    path('search', views.search, name='search'),
    path('settings', views.settings, name='settings'),
]