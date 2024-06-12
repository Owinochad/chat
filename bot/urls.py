from django.urls import path
from . import views 
from . views import *

urlpatterns=[
    path('', views.index, name = 'index'),
    path('uploadimage/',views.image_upload, name = 'uploadimage'),
    path('chat_view/', views.chat_view, name='chat_view'),
    path('result/', views.result, name='result'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(template_name = 'signup.html'), name='signup'),
    path('help/', views.help, name='help'),
    path('feedback/', views.feedback, name='feedback'),
    path('feedsuccess/', views.feedsuccess, name='feedsuccess'),
]
