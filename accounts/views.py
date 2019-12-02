from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, PasswordChangeForm
from .forms import CustomUserCreationForm
from django.views.decorators.http import require_POST


def signup(request):
    if request.user.is_authenticated:
        redirect('articles:index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('articles:index')
    else: # GET 
        form = CustomUserCreationForm() # 빈 UserCreationForm 보여줌
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
    
@login_required
def update(request):
    if request.method == 'POST':
        change_form = UserChangeForm(data=request.POST, instance=request.user)
        if change_form.is_valid():
            change_form.save()
            return redirect('articles:index')
    else: # GET 요청 : form 보여주기
        # 기존 정보가 담긴 form 
        change_form = UserChangeForm(instance=request.user)
    context = {'change_form': change_form}
    return render(request, 'accounts/update.html', context)


@login_required
# password 는 회원정보 수정에서 할 수 없음 (장고 기본 세팅)
# password 라는 url, view 함수 필요
def password(request):
    if request.method == 'POST':
        pass
    else:
        psw_form = PasswordChangeForm()
        context = {'psw_form': psw_form}
        return render(request, 'accounts/password.html', context)