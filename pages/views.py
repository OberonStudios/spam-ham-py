from django.shortcuts import redirect
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .models import Post
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.conf import settings
from django.views.generic.base import TemplateView
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

class base_posts(TemplateView):
    template_name = 'base_posts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        context['posts'] = posts
        return context


class base_post(TemplateView):
    template_name = 'base_post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post, pk=kwargs['pk'])
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        context['post'] = post
        return context

class base_dashboard(TemplateView):
    template_name = 'base_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        context['posts'] = posts
        context['statistics'] = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date').count()
        return context

def stripe_paid(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        stripe_paid = stripe.Charge.create(
            amount=post.price,
            currency='usd',
            description='Test Charge',
            source=request.POST['stripeToken']
        )
        return render(request, 'stripe_paid.html', {'post': post})

def base_index(request):
    return render(request, 'base_index.html')

# @staff_member_required
def base_post_add(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            import antispam
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.spam_score = str(antispam.score(post.text))
            post.save()
            return redirect('base_post', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'base_post_add.html', {'form': form})

# @staff_member_required
def base_post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('base_post', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'base_post_edit.html', {'form': form})


def base_auth_reg(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('base_posts')
    else:
        form = UserCreationForm()
    return render(request, 'base_auth_reg.html', {'form': form})


@login_required
def base_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('base_post', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'base_comment.html', {'form': form})
