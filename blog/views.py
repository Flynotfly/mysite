# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.views.decorators.http import require_POST
from .models import Post
from .forms import EmailPostForm, CommentForm


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 5
    template_name = 'blog/post/list.html'


# def post_list(request):
#     post_list = Post.published.all()
#     # Pagination with 5 post per page
#     paginator = Paginator(post_list, 5)
#     page_number = request.GET.get('page', 1)
#     try:
#         posts = paginator.page(page_number)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     except EmptyPage:
#         # get last page if page_number out of range
#         posts = paginator.page(paginator.num_pages)
#
#     return render(
#         request,
#         'blog/post/list.html',
#         {'posts': posts}
#     )


def post_detail(request, id, post):
    post = get_object_or_404(
        Post,
        id=id,
        slug=post,
        status=Post.Status.PUBLISHED,
    )

    comments = post.comments.filter(active=True)
    form_for_new_comment = CommentForm()

    return render(
        request,
        'blog/post/detail.html',
        {
            'post': post,
            'comments': comments,
            'form': form_for_new_comment,
        }
    )


def post_share(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED,
    )

    sent = False

    if request.method == 'POST':
        # form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = (
                f"{cd['name']} ({cd['email']})"
                f"recommends you read {post.title}"
            )
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}\'s comments: {cd['comments']}"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd['to']]
            )
            sent = True
    else:
        form = EmailPostForm()

    return render(
        request,
        'blog/post/share.html',
        {
            'post': post,
            'form': form,
            'sent': sent,
        }
    )


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED,
    )
    comment = None

    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

    return render(
        request,
        'blog/post/comment.html',
        {
            'post': post,
            'form': form,
            'comment': comment,
        }
    )
