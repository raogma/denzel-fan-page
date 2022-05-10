from django.urls import path

from DenzelProject.blogPost.views import DashView, CreatePostView, PostDetailsView, DeletePostView, EditPostView, \
    like_fn, dislike_fn
from DenzelProject.blogPost.commentView import CommentsViewREST, CommentDetailRest, CommentTemplate

urlpatterns = [
    path('', DashView.as_view(), name='posts'),
    path('create/', CreatePostView.as_view(), name='create-post'),
    path('edit/<int:pk>', EditPostView.as_view(), name='edit-post'),
    path('delete/<int:pk>', DeletePostView.as_view(), name='delete-post'),
    path('details/<int:pk>', PostDetailsView.as_view(), name='post-details'),
    path('details/<int:pk>/comments/', CommentTemplate.as_view(), name='comments'),
    path('details/<int:pk>/commentsREST/', CommentsViewREST.as_view(), name='comments-list-REST'),
    path('details/<int:pk>/commentsREST/<int:commentPk>/', CommentDetailRest.as_view(), name='comments-details-REST'),
    path('details/<int:pk>/like/', like_fn, name='post-details-like'),
    path('details/<int:pk>/dislike/', dislike_fn, name='post-details-dislike'),
]
