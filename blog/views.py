from django.shortcuts import render, get_object_or_404
from .models import *
from .forms import PostForm, CommentForm, UpdateForm, NewUserForm
from django.shortcuts import redirect, reverse
from django.utils import timezone
# from taggit.models import Tag
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views.generic import ListView

# from django.contrib.auth.decorators import login_required
# Import User UpdateForm, ProfileUpdatForm


def post_list(request):
    post = Post.objects.order_by('-published_date')
    # common_tags = Post.tags.most_common()
    return render(request, 'blog/post_list.html', {'post': post})


def post_detail(request, slug):
    template_name = 'blog/post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True, reply__isnull=True)
    print('lkkkkkkkkkkkkkkkkkkk')
    # Comment posted
    if request.method == 'POST':
        # comment has been added
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            parent_obj = None
            # get parent comment id from hidden input
            try:
                # id integer e.g. 15
                parent_id = int(request.POST.get('reply_id'))
            except:
                parent_id = None
            # if parent_id has been submitted get parent_obj id
            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)
                # if parent object exist
                if parent_obj:
                    # create replay comment object
                    replay_comment = comment_form.save(commit=False)
                    print(replay_comment, 'okkk')
                    # assign parent_obj to replay comment
                    replay_comment.reply = parent_obj
            # normal comment
            # create comment object but do not save to database
            new_comment = comment_form.save(commit=False)
            # assign ship to the comment
            new_comment.post = post
            # save
            print(new_comment, 'sssssss')

            new_comment.save()
            return redirect('blog:post_detail', slug=slug)
    else:
        comment_form = CommentForm()
    return render(request,
                  template_name,
                  {'post': post,
                   'comments': comments,
                   'comment_form': comment_form})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            print("Essssssssssssssssssss")
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'blog/postnew.html', {'form': form})


def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def add_category(request):
    category = Category.objects.all()
    return render(request, 'blog/add_category.html', {'category': category})
    # category = get_object_or_404(category, slug=slug)
    # print(category)
    # return render(request, 'blog/add_category.html', {'category': category})


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    post = Post.objects.filter(category=category)
    print(category, post)
    return render(request, 'blog/category_detail.html', {'post': post})


def tagged(request):
    tag = Tag.objects.all()
    return render(request, 'blog/add_tag.html', {'tag': tag})


def tag_detail(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    post = Post.objects.filter(tag=tag)
    print(tag, post)
    return render(request, 'blog/tag_detail.html', {'post': post})


def signup(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blog:login')
    else:
        form = NewUserForm()   
    return render(request, 'blog/signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        print(form)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(username, password)
            user = authenticate(username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('blog:post_list')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect("/")


def profile(request):
    profile = User.objects.all()
    return render(request, 'blog/profile.html', {'profile': profile})


def update(request):
    if request.method == "POST":
        form = UpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form = form.save(commit=False)
            request.form = request.user
            form.save()
            return redirect('blog:profile')
    else:
        form = UpdateForm(instance=request.user)
        return render(request, 'blog/update.html', {'form': form})
