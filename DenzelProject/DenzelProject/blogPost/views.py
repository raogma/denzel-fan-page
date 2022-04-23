from django.contrib.staticfiles import finders
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.core.cache import cache
from DenzelProject.blogPost.forms import CreatePostForm, SearchDashForm, DeletePostForm, CommentForm, DelCommentForm, \
    UpCommentForm
from DenzelProject.blogPost.models import Post, Comment, Like, Dislike
from DenzelProject.utils import ReloadSamePageMixin, check_opposite_liking_exists, save_liking, \
    check_same_liking_exists


class DashView(ListView):
    template_name = 'dashboard.html'
    model = Post
    paginate_by = 8

    def get_queryset(self):
        queryset_posts = cache.get('queryset')
        if queryset_posts is None:
            queryset_posts = super().get_queryset().select_related('owner').order_by('-created')
            cache.set('queryset', queryset_posts)

        title_filter = self.request.GET.get('searched')
        if title_filter:
            queryset_posts = queryset_posts.filter(header__contains=title_filter)
        return queryset_posts

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['form'] = SearchDashForm
        return ctx


def like_fn(req, pk):
    check_opposite_liking_exists(req, pk, Dislike)
    if check_same_liking_exists(req, pk, Like) != 'deleted':
        save_liking(req, pk, Like)
    return redirect('post-details', pk)


def dislike_fn(req, pk):
    check_opposite_liking_exists(req, pk, Like)
    if check_same_liking_exists(req, pk, Dislike) != 'deleted':
        save_liking(req, pk, Dislike)

    return redirect('post-details', pk)


class CommentsView(LoginRequiredMixin, CreateView, ListView, ReloadSamePageMixin):
    template_name = 'posts/comments.html'
    model = Comment
    form_class = CommentForm
    paginate_by = 3

    def get_success_url(self):
        return self.get_same_url()

    def get_context_data(self, **kwargs):
        queryset = kwargs.pop('object_list', None)
        if queryset is None:
            self.object_list = self.model.objects.select_related(
                'post').filter(post_id=self.kwargs['pk']).order_by('-created')
        ctx = super().get_context_data(**kwargs)
        ctx['post_pk'] = self.kwargs['pk']
        return ctx

    def get_queryset(self):
        queryset_comments = cache.get('queryset_comments')
        if queryset_comments is None:
            post_pk = self.kwargs['pk']
            queryset_comments = super().get_queryset()\
                                    .select_related('post')\
                                    .filter(post_id=post_pk)\
                                    .order_by('-created')
            cache.set('queryset_comments', queryset_comments)
        return queryset_comments

    def form_valid(self, form):
        res = super().form_valid(form)
        obj = form.save(commit=False)

        obj.post_id = int(self.kwargs['pk'])
        obj.owner_id = self.request.user.pk
        obj.save()
        return res


class EditCommentView(LoginRequiredMixin, UpdateView, ListView, ReloadSamePageMixin):
    template_name = 'posts/comments.html'
    model = Comment
    form_class = UpCommentForm
    paginate_by = 3

    def get_queryset(self):
        queryset_comments = cache.get('queryset_comments')
        if queryset_comments is None:
            post_pk = self.kwargs['pk']
            queryset_comments = super().get_queryset()\
                                    .select_related('post')\
                                    .filter(post_id=post_pk)\
                                    .order_by('-created')
            cache.set('queryset_comments', queryset_comments)
        return queryset_comments

    def get_object(self, queryset=None):
        return Comment.objects.get(id=self.kwargs['comment'])

    def get_success_url(self):
        return self.get_same_url()

    def get_context_data(self, **kwargs):
        queryset = kwargs.pop('object_list', None)
        if queryset is None:
            self.object_list = self.model.objects.select_related('post').filter(post_id=self.kwargs['pk']).order_by('-created')
        ctx = super().get_context_data(**kwargs)
        ctx['post_pk'] = self.kwargs['pk']
        return ctx


def delete_comment(request, pk, comment):
    comment = Comment.objects.get(id=comment)
    comment.delete()
    return redirect('post-details-comments', pk)


# class DeleteCommentView(LoginRequiredMixin, DeleteView, ListView, ReloadSamePageMixin, LoadCommentsMethodsMixin):
#     template_name = 'posts/comments.html'
#     model = Comment
#     form_class = DelCommentForm
#     paginate_by = 3

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         queryset = self.load_queryset(queryset)
#         return queryset

#     def get_object(self, queryset=None):
#         return Comment.objects.get(id=self.kwargs['comment'])

#     def get_success_url(self):
#         return self.get_same_url()

#     def get_initial(self):
#         return {'content': self.object.content}

#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#         self.load_ctx(ctx)
#         return ctx


class PostDetailsView(DetailView):
    template_name = 'posts/post-details.html'
    model = Post

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx['owner'] = self.object.owner.profile
        ctx['comments_count'] = Comment.objects\
            .select_related('post').filter(post=self.object).count()
        ctx['likes_count'] = Like.objects\
            .select_related('post').filter(post=self.object).count()
        ctx['dislikes_count'] = Dislike.objects\
            .select_related('post').filter(post=self.object).count()

        return ctx


class CreatePostView(LoginRequiredMixin, CreateView):
    form_class = CreatePostForm
    template_name = 'posts/create-post.html'
    success_url = reverse_lazy('posts')

    def form_valid(self, form):
        res = super().form_valid(form)
        obj = form.save(commit=False)
        obj.owner_id = self.request.user.pk
        obj.save()
        return res


class EditPostView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = CreatePostForm
    template_name = 'posts/edit-post.html'

    def get_success_url(self):
        return reverse_lazy('post-details', kwargs={'pk': self.object.pk})


class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    form_class = DeletePostForm
    template_name = 'posts/delete-post.html'

    def get_initial(self):
        return {
            'header': self.object.header,
            'description': self.object.description,
        }

    def get_success_url(self):
        return reverse_lazy('posts')
