import factory
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from .models import Category, Tag, Post, Comment

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("username",)

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ("name",)

    name = factory.Faker("word")
    description = factory.Faker("sentence")
    # slug is handled automatically by your model's save() method


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag
        django_get_or_create = ("name",)

    name = factory.Faker("word")
    # slug is handled automatically by your model's save() method


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.Faker("sentence", nb_words=6)
    excerpt = factory.Faker("text", max_nb_chars=200)
    content = factory.Faker("paragraph", nb_sentences=10)
    featured_image = factory.django.ImageField(
        color="blue"
    )  # Generates a dummy image file
    author = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)
    reading_time = factory.Faker("random_int", min=1, max=15)
    status = factory.Iterator(
        [Post.Status.PUBLISHED, Post.Status.PUBLISHED, Post.Status.DRAFT]
    )

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for tag in extracted:
                self.tags.add(tag)
        else:
            # Add 1 to 3 random tags if none are explicitly provided
            import random

            tags_pool = Tag.objects.all()
            if tags_pool.exists():
                num_tags = min(random.randint(1, 3), tags_pool.count())
                self.tags.add(*random.sample(list(tags_pool), num_tags))


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    post = factory.SubFactory(PostFactory)
    full_name = factory.Faker("name")
    email = factory.Faker("email")
    website = factory.Faker("url")
    comment = factory.Faker("paragraph", nb_sentences=3)
    is_approved = factory.Faker(
        "boolean", chance_of_getting_true=80
    )  # 80% chance to be approved
