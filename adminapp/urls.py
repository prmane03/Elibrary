
from django.contrib import admin
from django.urls import path
from adminapp import views

urlpatterns = [
    path('', views.index , name='landingpg'),
    path('signup', views.signup , name='signuppg'),
    path('signin', views.signin , name='signinpg'),
    path('dashboard', views.dashboard , name='dashbordpg'),
    path('addbook', views.addbook , name='addbook'),
    path('updatebook', views.updatebook , name='updatebook'),
    path('logout', views.logout , name='logout'),
    path('deletebook', views.deletebook , name='deletebook'),
    path('account', views.account , name='account'),
    path('completeprofile', views.completeprofile , name='completeprofile'),
    path('editprofile', views.editprofile , name='editprofile'),
    path('showbook', views.showbook , name='showbook'),
]