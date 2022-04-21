from django.contrib import admin
from django.contrib.auth import get_user_model

from DenzelProject.blogPost.models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('header', 'description', 'owner', 'created')


@admin.register(get_user_model())
class User(admin.ModelAdmin):
    def group(self, user):
        groups = []
        for group in user.groups.all():
            groups.append(group.name)
        return ' '.join(groups)

    # group.short_description = 'Groups'
    list_display = ('email', 'group', 'is_staff', 'is_superuser')


@admin.register(Comment)
class Comment(admin.ModelAdmin):
    list_display = ('content', 'post', 'owner', 'created')
