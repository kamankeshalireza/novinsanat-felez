from django.contrib.sitemaps import Sitemap

from .models import Category, Post, Tag


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Post.objects.filter(status=Post.Status.PUBLISHED).order_by("-created_at")

    def lastmod(self, obj):
        return obj.updated_at


class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Category.objects.all()


class TagSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.3

    def items(self):
        return Tag.objects.all()
