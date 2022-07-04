from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ModelSerializer
from DenzelProject.blogPost.models import Comment
from rest_framework.pagination import PageNumberPagination


class CommentsSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CommentsREST(ListCreateAPIView):
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
    permission_classes = (IsAuthenticated,)
    
    def get_object(self):
        return Comment.objects.get(id=self.kwargs['commentPk']) 
