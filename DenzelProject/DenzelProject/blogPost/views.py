from django.contrib.staticfiles import finders
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models.fields.files import ImageFieldFile, FileField, ImageField
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView

from DenzelProject.blogPost.forms import CreatePostForm, SearchDashForm, DeletePostForm, CommentForm, DelCommentForm, \
    UpCommentForm
from DenzelProject.blogPost.models import Post, Comment, Like, Dislike
from DenzelProject.utils import ReloadSamePageMixin, check_opposite_liking_exists, save_liking, LoadCommentsContextDataMixin


class DashView(ListView):
    template_name = 'dashboard.html'
    model = Post
    paginate_by = 8

    def get_queryset(self):
        return super().get_queryset().select_related('owner')

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['form'] = SearchDashForm
        return ctx


def like_fn(req, pk):
    check_opposite_liking_exists(req, pk, Dislike)
    save_liking(req, pk, Like)
    return redirect('post-details', pk)


def dislike_fn(req, pk):
    check_opposite_liking_exists(req, pk, Like)
    save_liking(req, pk, Dislike)
    return redirect('post-details', pk)


class CommentsView(LoginRequiredMixin, CreateView, ReloadSamePageMixin, LoadCommentsContextDataMixin):
    template_name = 'posts/comments.html'
    model = Comment
    form_class = CommentForm

    def get_success_url(self):
        return self.get_same_url()

    def form_valid(self, form):
        res = super().form_valid(form)
        obj = form.save(commit=False)

        obj.post_id = int(self.kwargs['pk'])
        obj.owner_id = self.request.user.pk
        obj.save()
        return res

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        self.load_ctx(ctx)
        return ctx


class DeleteCommentView(LoginRequiredMixin, DeleteView, ReloadSamePageMixin, LoadCommentsContextDataMixin):
    template_name = 'posts/comments.html'
    model = Comment
    form_class = DelCommentForm

    def get_object(self, queryset=None):
        return Comment.objects.get(id=self.kwargs['comment'])

    def get_success_url(self):
        return self.get_same_url()

    def get_initial(self):
        return {'content': self.object.content}

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        self.load_ctx(ctx)
        return ctx


class EditCommentView(LoginRequiredMixin, UpdateView, ReloadSamePageMixin, LoadCommentsContextDataMixin):
    template_name = 'posts/comments.html'
    model = Comment
    form_class = UpCommentForm

    def get_object(self, queryset=None):
        return Comment.objects.get(id=self.kwargs['comment'])

    def get_success_url(self):
        return self.get_same_url()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        self.load_ctx(ctx)
        return ctx


class PostDetailsView(DetailView):
    template_name = 'posts/post-details.html'
    model = Post

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['owner'] = self.object.owner.profile
        ctx['comments_count'] = self.object.comment_set.count()
        ctx['likes_count'] = self.object.like_set.count()
        ctx['dislikes_count'] = self.object.dislike_set.count()
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
            'image': self.object.image,
            'header': self.object.header,
            'description': self.object.description,
        }

    def get_success_url(self):
        return reverse_lazy('posts')
