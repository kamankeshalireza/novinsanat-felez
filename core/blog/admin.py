from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Comment, Post, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "post_count")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}

    def get_queryset(self, request):
        from django.db.models import Count

        return super().get_queryset(request).annotate(_post_count=Count("posts"))

    @admin.display(description="Posts")
    def post_count(self, obj):
        return obj._post_count


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ("full_name", "email", "comment", "is_approved", "parent", "created_at")
    readonly_fields = ("created_at",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "category",
        "status",
        "reading_time",
        "created_at",
        "thumbnail",
    )
    list_filter = ("status", "category", "tags", "created_at")
    search_fields = ("title", "excerpt", "content")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("author", "category", "tags")
    date_hierarchy = "created_at"
    inlines = [CommentInline]

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("author", "category")
            .prefetch_related("tags")
        )

    @admin.display(description="Image")
    def thumbnail(self, obj):
        if obj.featured_image:
            return format_html(
                '<img src="{}" style="height:40px;border-radius:4px;" />',
                obj.featured_image.url,
            )
        return "-"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("full_name", "post", "is_approved", "created_at", "parent")
    list_filter = ("is_approved", "created_at")
    search_fields = ("full_name", "email", "comment")
    actions = ["approve_comments", "disapprove_comments"]
    autocomplete_fields = ("post", "parent")

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("post", "parent")

    @admin.action(description="Approve selected comments")
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)

    @admin.action(description="Disapprove selected comments")
    def disapprove_comments(self, request, queryset):
        queryset.update(is_approved=False)
