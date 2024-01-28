from django.urls import path
from . import views

urlpatterns = [
    path('',views.BookList.as_view()),
    path('<int:pk>/', views.BookDetail.as_view()),
    path('category/<str:slug1>/<str:slug2>/',views.genre_page),
    path('create_item/', views.BookCreate.as_view()),
    path('create_author/',views.AuthorCreate.as_view()),
    path('update_item/<int:pk>/',views.BookUpdate.as_view()),
    path('author/<str:slug>/',views.author_page),
    path('publisher_page/<str:slug>/',views.publisher_page),
    path('my_page/',views.my_page),
    path('<int:pk>/new_comment/',views.new_comment),
    path('update_comment/<int:pk>/',views.CommentUpdate.as_view()),
    path('delete_comment/<int:pk>/',views.delete_comment),
    path('search/<str:q>/',views.BookSearch.as_view()),
    path('main/',views.main),
    path('about/',views.about),
    path('<int:pk1>/comment/<int:pk2>/new_commentofcomment/',views.new_commentofcomment),
    path('update_coc/<int:pk>/',views.CommentOfCommentUpdate.as_view()),
    path('delete_coc/<int:pk>/',views.delete_coc),
    path('keyword/<str:slug>/',views.keyword_page)
]