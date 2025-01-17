from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm

class PostListView(ListView):
    queryset = Post.objects.filter(status="published")
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post_list.html"

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published',
                             publish__year=year, publish__month=month, publish__day=day)
    
    comments = post.comments.filter(active=True)
    new_comment = None  
    
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()

    else:
        comment_form = CommentForm()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,  # Corrected variable name
        'comment_form': comment_form
    })
    
    

def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status="published")
    sent = False

    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, "nanakwesiwalker2020@gmail.com", [cd["email"]])
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'blog/post_share.html', {'post': post, 'form': form, 'sent': sent})
