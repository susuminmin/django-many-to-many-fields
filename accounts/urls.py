from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signout/', views.signout, name='signout'),
    path('update/', views.update, name='update'),
    path('password/', views.password, name='password'),
]
