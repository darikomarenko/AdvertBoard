from django.urls import path

from adverts.views import *

urlpatterns = [
    path('posts/', PostListView.as_view(), name='posts_list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post'),
    path('posts/<int:pk>/post_del_ask/', post_delete_ask, name='post_del_ask'),
    path('posts/<int:pk>/post_del_ask/post_del_confirm/', post_delete_confirm, name='post_del_confirm'),
    path('posts/<int:pk>/reply_del_ask/<int:reply_pk>/', reply_delete_ask, name='reply_del_ask'),
    path('posts/<int:pk>/reply_del_ask/<int:reply_pk>/reply_del_confirm/', reply_delete_confirm, name='reply_del_confirm'),
    path('posts/<int:pk>/repl_apr_and_disapr/<int:reply_pk>/', reply_approve_and_disapprove, name='reply_apr_and_disapr'),
    path('posts/<int:pk>/reply_rej_and_unrej/<int:reply_pk>/', reply_reject_and_unreject, name='reply_rej_and_unrej'),
    path('posts_search/', PostSearchView.as_view(), name='posts_search'),
    path('post_create/', PostCreateView.as_view(), name='post_create'),
    path('post_update/<int:pk>/', PostUpdateView.as_view(), name='post_update'),
    path('profile_posts/<int:pk>/', ProfilePostsView.as_view(), name='profile_posts'),
    path('profile_replies/<int:pk>/', ProfileRepliesView.as_view(), name='profile_replies'),
]
