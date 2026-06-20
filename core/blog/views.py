from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormMixin

from .forms import CommentForm
from .models import Category, Post, Tag

User = get_user_model()

PAGINATE_BY = 6


class BlogSidebarMixin:
    """Provides common sidebar context data (categories, tags, recent posts)."""

    def get_sidebar_context(self):
        categories = Category.objects.annotate(
            post_count=Count(
                "posts", filter=Q(posts__status=Post.Status.PUBLISHED), distinct=True
            )
        ).order_by("name")

        tags = Tag.objects.annotate(
            post_count=Count(
                "posts", filter=Q(posts__status=Post.Status.PUBLISHED), distinct=True
            )
        ).order_by("name")

        recent_posts = (
            Post.objects.filter(status=Post.Status.PUBLISHED)
            .select_related("author", "category")
            .order_by("-created_at")[:5]
        )

        return {
            "categories": categories,
            "tags": tags,
            "recent_posts": recent_posts,
        }


class PostListView(BlogSidebarMixin, ListView):
    """
    Handles the category.html template.
    Supports filtering by category slug, tag slug, author, and search query (q).
    """

    model = Post
    template_name = "blog/category.html"
    context_object_name = "post_list"
    paginate_by = PAGINATE_BY

    def get_queryset(self):
        queryset = (
            Post.objects.filter(status=Post.Status.PUBLISHED)
            .select_related("author", "category")
            .prefetch_related("tags")
        )

        category_slug = self.kwargs.get("category_slug")
        if category_slug:
            self.current_category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=self.current_category)
        else:
            self.current_category = None

        tag_slug = self.kwargs.get("tag_slug")
        if tag_slug:
            self.current_tag = get_object_or_404(Tag, slug=tag_slug)
            queryset = queryset.filter(tags=self.current_tag)
        else:
            self.current_tag = None

        author_param = self.kwargs.get("author") or self.request.GET.get("author")
        self.current_author = None
        if author_param:
            author_lookup = Q(username=author_param)
            if str(author_param).isdigit():
                author_lookup |= Q(pk=author_param)
            self.current_author = get_object_or_404(User, author_lookup)
            queryset = queryset.filter(author=self.current_author)

        self.search_query = self.request.GET.get("q", "").strip()
        if self.search_query:
            queryset = queryset.filter(
                Q(title__icontains=self.search_query)
                | Q(excerpt__icontains=self.search_query)
                | Q(content__icontains=self.search_query)
            )

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_sidebar_context())
        context["current_category"] = self.current_category
        context["current_tag"] = self.current_tag
        context["current_author"] = self.current_author
        context["search_query"] = self.search_query
        return context


class PostDetailView(BlogSidebarMixin, FormMixin, DetailView):
    """
    Handles the blog-details.html template.
    Displays full post, approved nested comments, and processes CommentForm submissions.
    """

    model = Post
    template_name = "blog/blog-details.html"
    context_object_name = "post"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    form_class = CommentForm

    def get_queryset(self):
        return (
            Post.objects.filter(status=Post.Status.PUBLISHED)
            .select_related("author", "category")
            .prefetch_related("tags")
        )

    def get_success_url(self):
        return (
            reverse("blog:post_detail", kwargs={"slug": self.object.slug})
            + "#blog-comments"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_sidebar_context())

        comments_qs = (
            self.object.comments.filter(is_approved=True)
            .select_related("post")
            .prefetch_related("replies")
        )
        top_level_comments = comments_qs.filter(parent__isnull=True)

        context["comments"] = top_level_comments
        context["comments_count"] = comments_qs.count()
        if "form" not in context:
            context["form"] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.object
        comment.is_approved = False
        comment.save()
        messages.success(
            self.request,
            "Thank you! Your comment has been submitted and is awaiting moderation.",
        )
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)
