from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from .models import Article, Comment, Post
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import request
from .forms import CommentForm


#--------------------------------------------------------------------------#

class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'article_list.html'
    login_url = 'login'
    
    def get_queryset(self):
        query = self.request.GET.get('search')
        if query:
            QuerySet = Article.objects.filter(Q(title__icontains=query))
        else:
            QuerySet = super().get_queryset()
        return QuerySet

class ArticleDetailView(LoginRequiredMixin, DetailView): 
    model = Article
    template_name = 'article_detail.html'
    login_url = 'login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.get_object()
        comments = Comment.objects.filter(article=article)
        context['comments'] = comments
        context['comment_form'] = CommentForm()
        return context

class ArticleUpdateView(LoginRequiredMixin, UpdateView): 
    model = Article
    fields = ('title', 'body',)
    template_name = 'article_edit.html'
    login_url = 'login' 
    
    def dispatch(self, request, *args, **kwargs): 
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    
class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')
    login_url = 'login'
    
    def dispatch(self, request, *args, **kwargs): # new
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'article_new.html'
    fields = ('title', 'body',)
    login_url = 'login'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

class CommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comments.html'

    def form_valid(self, form):
        article_pk = self.kwargs['pk']
        article = get_object_or_404(Article, pk=article_pk)
        comment = form.save(commit=False)
        comment.article = article
        comment.author = self.request.user
        comment.save()
        
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article_pk = self.kwargs['pk']
        article = get_object_or_404(Article, pk=article_pk)
        comments = Comment.objects.filter(article=article)
        context['article'] = article
        context['comments'] = comments
        return context

    def get_success_url(self):
        article_pk = self.kwargs['pk']
        return reverse_lazy('articles_comments', kwargs={'pk': article_pk})




    
    
    
    

    


