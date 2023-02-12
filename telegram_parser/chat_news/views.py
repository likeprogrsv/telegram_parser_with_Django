from django.shortcuts import render
from .models import Tag, Post, Picture


def show_news(request):    
    tags = Tag.objects.all()
    
    img = Picture.objects.all()

    curr_tag = request.GET.get('curr_tag')
    if curr_tag is None:
        posts = Post.objects.all()
    else:
        posts = Post.objects.filter(tag__name__contains=curr_tag)

    context = {'tags': tags, 'posts': posts, }
    return render(request, 'chat_news/news.html', context)
