from django.urls import path

from DenzelProject.blogPost.views import DashView, CreatePostView, PostDetailsView, DeletePostView, EditPostView, \
    CommentsView, delete_comment, like_fn, dislike_fn, EditCommentView

urlpatterns = [
    path('', DashView.as_view(), name='posts'),
    path('create/', CreatePostView.as_view(), name='create-post'),
    path('edit/<int:pk>', EditPostView.as_view(), name='edit-post'),
    path('delete/<int:pk>', DeletePostView.as_view(), name='delete-post'),
    path('details/<int:pk>', PostDetailsView.as_view(), name='post-details'),
    path('details/<int:pk>/comments/', CommentsView.as_view(), name='post-details-comments'),
    path('details/<int:pk>/comments/edit/<int:comment>/', EditCommentView.as_view(), name='post-edit-comments'),
    path('details/<int:pk>/comments/delete/<int:comment>/', delete_comment, name='post-delete-comments'),
    path('details/<int:pk>/like/', like_fn, name='post-details-like'),
    path('details/<int:pk>/dislike/', dislike_fn, name='post-details-dislike'),
]
