from django.shortcuts import render
from .models import Tag, Post, Picture
from rest_framework import generics
from .serializers import PostSerializer, TagSerializer


class TagList(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class PostList(generics.ListAPIView):
    queryset = Post.objects.all().order_by('-post_time')
    serializer_class = PostSerializer


class PostByTag(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        tag = self.kwargs['tag']
        return Post.objects.filter(tag__name=tag).order_by('-post_time')


def show_news(request):
    tags = Tag.objects.all()
    curr_tag = request.GET.get('curr_tag')
    if curr_tag is None:
        posts = Post.objects.all()
    else:
        posts = Post.objects.filter(tag__name__contains=curr_tag)
    post_img = Picture.objects.all()

    context = {'tags': tags, 'posts': posts, 'imgs': post_img}
    return render(request, 'chat_news/news.html', context)
