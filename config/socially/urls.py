from django.urls import path
from . import views

app_name = 'socially'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('<str:this_user>', views.user_socials, name='user_socials')
]