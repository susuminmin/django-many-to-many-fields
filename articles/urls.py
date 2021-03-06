from django.urls import path
from . import views


app_name = 'articles'

urlpatterns = [
    # Article CRUD
    path('', views.index, name="index"),
    path('create/', views.create, name='create'),
    path('<int:article_pk>/', views.detail, name='detail'),
    path('<int:article_pk>/update/', views.update, name='update'),
    path('<int:article_pk>/delete/', views.delete, name='delete'),
    # Article 좋아요 기능
    path('<int:article_pk>/like/', views.like, name='like'),
    # Article 의 작성자를 Follow 하는 기능
    path('<int:article_pk>/follow/', views.follow, name='follow'),

    # Comment CRUD (R은 게시글 상세보기)
    path('<int:article_pk>/comment_create/', views.comment_create, name='comment_create'),
    path('<int:article_pk>/comment_delete/<int:comment_pk>/', views.comment_delete, name="comment_delete"),
    path('<int:article_pk>/comment_update/<int:comment_pk>/', views.comment_update, name="comment_update"),
]
