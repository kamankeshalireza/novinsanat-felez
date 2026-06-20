from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    # Main post list / search
    path("", views.PostListView.as_view(), name="post_list"),
    path("search/", views.PostListView.as_view(), name="post_search"),
    # Category filter
    path(
        "category/<slug:category_slug>/",
        views.PostListView.as_view(),
        name="category_filter",
    ),
    # Tag filter
    path("tag/<slug:tag_slug>/", views.PostListView.as_view(), name="tag_filter"),
    # Author filter (username or id)
    path("author/<str:author>/", views.PostListView.as_view(), name="author_filter"),
    # Post detail
    path("<slug:slug>/", views.PostDetailView.as_view(), name="post_detail"),
]
