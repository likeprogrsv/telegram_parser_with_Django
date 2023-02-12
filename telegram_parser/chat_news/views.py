from django.shortcuts import render
from .models import Tag, Post, Picture


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
