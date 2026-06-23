from django import template
from blog.models import Post, Category

register = template.Library()


@register.inclusion_tag("blog/components/featured_posts.py.html", takes_context=True)
def render_featured_posts(context, limit=5):
    """
    Renders the featured posts section slider.
    """
    # Grab published posts. Prefetch related categories/authors to optimize queries
    featured_posts = (
        Post.objects.filter(status=Post.Status.PUBLISHED)
        .select_related("category", "author")
        .order_by("-created_at")[:limit]
    )

    return {
        "request": context.get("request"),
        "featured_posts": featured_posts,
    }


@register.inclusion_tag("blog/components/category_section.html", takes_context=True)
def render_category_section(context, category_slug, section_title=None):
    """
    Fetches posts belonging to a specific category slug and chunks them
    for the specialized category grid layout.
    """
    context_data = {
        "request": context.get("request"),
        "category_name": section_title,
    }

    try:
        category = Category.objects.get(slug=category_slug)
        if not section_title:
            context_data["category_name"] = category.name

        # Fetch up to 9 published posts in this category
        posts = (
            Post.objects.filter(category=category, status=Post.Status.PUBLISHED)
            .select_related("author", "category")
            .order_by("-created_at")[:9]
        )

        # Slicing the single query to avoid database overhead
        context_data["hero_post"] = posts[0] if len(posts) > 0 else None
        context_data["sidebar_posts"] = posts[1:5] if len(posts) > 1 else []
        context_data["grid_posts"] = posts[5:9] if len(posts) > 5 else []

    except Category.DoesNotExist:
        context_data["category_name"] = section_title or "Unknown Category"
        context_data["hero_post"] = None
        context_data["sidebar_posts"] = []
        context_data["grid_posts"] = []

    return context_data


@register.inclusion_tag("blog/components/latest_posts.html", takes_context=True)
def render_latest_posts(context, limit=5):
    """
    Fetches the most recent published posts overall and splits them
    into a main left block and a right-side compact stack.
    """
    # Fetch latest posts up to your limit
    posts = (
        Post.objects.filter(status=Post.Status.PUBLISHED)
        .select_related("category", "author")
        .order_by("-created_at")[:limit]
    )

    return {
        "request": context.get("request"),
        "primary_post": posts[0] if len(posts) > 0 else None,
        "secondary_posts": posts[1:] if len(posts) > 1 else [],
    }
