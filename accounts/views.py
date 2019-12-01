from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.decorators.http import require_POST


def signup(request):
    if request.user.is_authenticated:
        redirect('articles:index')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('articles:index')
    else: # GET 
        form = UserCreationForm() # 빈 UserCreationForm 보여줌
    context = {'form': form}
    return render(request, 'accounts/signup.html', context)


def login_view(request):
    if request.user.is_authenticated:
        redirect('articles:index')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            next_page = request.GET.get('next')
            # index 페이지에서 로그인할 때 / 로그인이 필요한 일을 하려고 할 때
            return redirect('articles:index' or next_page)
    else: # GET
        form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'accounts/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('articles:index')


# 회원탈퇴
# @require_POST
def signout(request):
    if request.user.is_authenticated:
        request.user.delete()
    return redirect('articles:index')
    