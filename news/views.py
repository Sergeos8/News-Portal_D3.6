from django.shortcuts import render
from datetime import datetime
from django.views.generic import ListView, DetailView
from .models import *


class PostsList(ListView):
    model = Post
    template_name = 'news.html'
    ordering = '-date_created'
    context_object_name = "news"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_post'] = None
        return


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context
