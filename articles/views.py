from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from .models import Article, Comment
from .forms import ArticleForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


@require_GET
def index(request):
    articles = Article.objects.all()
    context = {'articles': articles}
    return render(request, 'articles/index.html', context)


@require_GET
def detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    # 기존 댓글과 댓글 생성 폼도 보여주어야 함
    comments = article.comments.all()
    comment_form = CommentForm()
    context = {
        'article': article,
        'comments': comments,
        'comment_form': comment_form,
        }
    return render(request, 'articles/detail.html', context)


@login_required
def create(request):
    if request.method == 'POST':
        # Article 을 생성해달라고 하는 요청
        form = ArticleForm(request.POST)
        if form.is_valid():
            # Article 모델에 user field 추가 후
            # form.save() 대신 다음 로직 구현
            article = form.save(commit=False) # 모델 반환 (title 과 content 만 쓴 상태)
            article.user = request.user # user field 에 지금 request 보낸 user 를 저장
            article.save() # 비로소 저장
            return redirect('articles:detail', article.pk)
        else:
            # invalid 한 정보 넣은 채 form 담은 페이지 보여주기
            context = {'form': form}
            return render(request, 'articles/create.html', context)
    else: # GET
        # Article 을 생성하기 위한 페이지를 달라고 하는 요청
        form = ArticleForm() # 빈 form 생성
        context = {'form': form}
        return render(request, 'articles/create.html', context)


# login page 로 redirect 하는 decorator
@login_required
def update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if article.user == request.user:
        if request.method == 'POST':
            form = ArticleForm(request.POST, instance=article)
            if form.is_valid():
                form.save()
                return redirect('articles:detail', article_pk)
        else: # GET 
            # 기존 정보가 담긴 폼을 보여줘야 함... 
            form = ArticleForm(instance=article)
        context =  {'form': form}
        return render(request, 'articles/update.html', context)
    else: # 글 작성자 본인이 아닌 경우
        return redirect('articles:detail', article_pk)


# articles/3/delete/ 로 url 에 직접 칠 때 삭제가 되지 않도록
@require_POST
def delete(request, article_pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=article_pk)
        if article.user == request.user:
            article.delete()
        else:
            return redirect('articles:detail', article_pk)
    return redirect('articles:index')


@require_POST
def comment_create(request, article_pk):
    if request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid(): # fields 에 article 정보 없었음
            comment = form.save(commit=False) # instance 를 반환
            comment.article_id = article_pk
            comment.user = request.user
            comment.save()
    return redirect('articles:detail', article_pk)


# Article Delete 와 마찬가지로 url 삭제 불가능하도록
@require_POST
def comment_delete(request, article_pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if comment.user == request.user:
            comment.delete()
        return redirect('articles:detail', article_pk)
    else:
        return HttpResponse('You are unauthorized', status=401)


@login_required
def comment_update(request, article_pk, comment_pk):
    article = get_object_or_404(Article, pk=article_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)
    comments = Comment.objects.all()
    empty_form = CommentForm()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST, instance=comment)
        if comment_form.is_valid:
            comment_form.save()
            return redirect('articles:detail', article_pk)
    else: # GET
        comment_form = CommentForm(instance=comment)
    context = {
        'empty_form': empty_form,
        'article': article,
        'comment': comment,
        'comments': comments,
        'comment_form': comment_form,
        'comment_pk': comment_pk, # flag 역할
        }
    return render(request, 'articles/comment_update.html', context)
    

# 특정 게시글 좋아요 기능 (detail 페이지에 표시)
@login_required
def like(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    # if request.user not in article.like_users:
    if article.like_users.filter(pk=request.user.pk).exists():
        article.like_users.remove(request.user)
    else:
        article.like_users.add(request.user)
    return redirect('articles:detail', article_pk)


@login_required
def follow(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    reader = request.user # article 보는 중인 사람...
    # reader 가 article.user 를 follow 하려고 함
    if article.user != reader:
        if reader in article.user.followers.all():
            article.user.followers.remove(reader)
        else:
            article.user.followers.add(reader)
    return redirect('articles:detail', article_pk)
