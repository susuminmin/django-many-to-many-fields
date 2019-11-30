from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from .models import Article, Comment
from .forms import ArticleForm, CommentForm


@require_GET
def index(request):
    articles = Article.objects.all()
    context = {'articles': articles}
    return render(request, 'articles/index.html', context)


@require_GET
def detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    # 기존 댓글과 댓글 생성 폼도 보여주어야 함
    comments = Comment.objects.all()
    comment_form = CommentForm()
    context = {
        'article': article,
        'comments': comments,
        'comment_form': comment_form,
        }
    return render(request, 'articles/detail.html', context)


def create(request):
    if request.method == 'POST':
        # Article 을 생성해달라고 하는 요청
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('articles:index')
        else:
            # invalid 한 정보 넣은 채 form 담은 페이지 보여주기
            context = {'form': form}
            return render(request, 'articles/create.html', context)
    else: # GET
        # Article 을 생성하기 위한 페이지를 달라고 하는 요청
        form = ArticleForm() # 빈 form 생성
        context = {'form': form}
        return render(request, 'articles/create.html', context)


def update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
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


# articles/3/delete/ 로 url 에 직접 칠 때 삭제가 되지 않도록
@require_POST
def delete(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    article.delete()
    return redirect('articles:index')


@require_POST
def comment_create(request, article_pk):
    form = CommentForm(request.POST)
    if form.is_valid(): # fields 에 article 정보 없었음
        comment = form.save(commit=False) # instance 를 반환
        comment.article_id = article_pk
        comment.save()
    return redirect('articles:detail', article_pk)


# Article Delete 와 마찬가지로 url 삭제 불가능하도록
@require_POST
def comment_delete(request, article_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    comment.delete()
    return redirect('articles:detail', article_pk)


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
        'comment_pk': comment_pk, 
        }
    return render(request, 'articles/comment_update.html', context)
    