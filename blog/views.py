from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from .models import Post


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
    return render(
        request,
        'blog/post/detail.html',
        {'post': post}
    )
