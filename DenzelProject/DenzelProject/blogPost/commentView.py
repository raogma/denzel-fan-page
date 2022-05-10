from xml.dom.pulldom import COMMENT
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import ModelSerializer
from django.views.generic import TemplateView
from DenzelProject.blogPost.models import Comment
from rest_framework.pagination import PageNumberPagination


class CommentsSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CommentsViewREST(ListCreateAPIView):
    serializer_class = CommentsSerializer
    queryset = Comment.objects.select_related('post').all()
    pagination_class = PageNumberPagination

    def get_queryset(self):
        post_pk = self.kwargs['pk']                                
        return self.queryset \
            .select_related('post')\
            .filter(post_id=post_pk)\
            .order_by('-created')


class CommentDetailRest(RetrieveUpdateDestroyAPIView):
    serializer_class = CommentsSerializer
    
    def get_object(self):
        comment = Comment.objects.get(id=self.kwargs['commentPk']) 
        return comment


class CommentTemplate(TemplateView):
    template_name = 'posts/comments.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['post_pk'] = kwargs['pk']
        return ctx
