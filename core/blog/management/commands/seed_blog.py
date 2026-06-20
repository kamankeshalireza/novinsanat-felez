import random
from django.core.management.base import BaseCommand
from django.db import transaction
from ...factories import (
    UserFactory,
    CategoryFactory,
    TagFactory,
    PostFactory,
    CommentFactory,
)
from ...models import Category, Tag, Post, Comment


class Command(BaseCommand):
    help = "Seeds the database with fake blog data"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        # Optional: Clear existing data to start fresh (careful in production!)
        Comment.objects.all().delete()
        Post.objects.all().delete()
        Category.objects.all().delete()
        Tag.objects.all().delete()

        self.stdout.write("Creating fake data...")

        # 1. Create Categories and Tags first
        categories = [CategoryFactory() for _ in range(5)]
        tags = [TagFactory() for _ in range(10)]

        # 2. Create Posts
        posts = []
        for _ in range(20):
            post = PostFactory(category=random.choice(categories))
            posts.append(post)

        # 3. Create Top-level Comments and Nested Replies
        for post in posts:
            # Generate 2 to 5 top-level comments per post
            for _ in range(random.randint(2, 5)):
                parent_comment = CommentFactory(post=post, parent=None)

                # 50% chance to generate 1 or 2 nested replies to this comment
                if random.choice([True, False]):
                    for _ in range(random.randint(1, 2)):
                        CommentFactory(post=post, parent=parent_comment)

        self.stdout.write(
            self.style.SUCCESS(f"Successfully seeded {len(posts)} posts and comments!")
        )
