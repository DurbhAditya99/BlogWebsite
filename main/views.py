from django.shortcuts import render,redirect,get_object_or_404
from .models import BlogPost,Comments
from .forms import PostForm,CommentForm
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import (TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView)
# Create your views here.

class AboutView(TemplateView):
	template_name= 'main/about.html'

class PostListView(ListView):
    model=BlogPost
	
class PostDetailView(DetailView):
	model=BlogPost



class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'main/post_list.html'

    form_class = PostForm

    model = BlogPost

class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'main/post_detail.html'

    form_class = PostForm

    model = BlogPost

class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'main/post_list.html'
    template_name= 'main/post_draft_list.html'
    model = BlogPost
    context_object_name='blogposts'
    def get_queryset(self):
        return BlogPost.objects.filter(published_date__isnull=True).order_by('date')

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = BlogPost
    success_url = reverse_lazy('post_list')
    
##############################################################
#############################################################
@login_required
def post_publish(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)   

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
    	form = CommentForm()
    return render(request, 'main/comment_form.html', {'form': form}) 

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comments, pk=pk)
    post_pk=comment.post.pk
    comment.approve()
    return redirect('post_detail', pk=post_pk)

def comment_remove(request,pk):
	comment= get_object_or_404(Comment, pk=pk)
	post_pk=comment.post.pk
	comment.delete()
	return redirect('post_detail', pk=post_pk)