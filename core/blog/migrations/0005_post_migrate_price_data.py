from django.db import migrations


def copy_price_forward(apps, schema_editor):
    Post = apps.get_model('blog', 'Post')
    for post in Post.objects.all():
        raw = (post.price or '').strip()
        post.price_new = int(raw) if raw.isdigit() else None
        post.save(update_fields=['price_new'])


def copy_price_backward(apps, schema_editor):
    Post = apps.get_model('blog', 'Post')
    for post in Post.objects.all():
        post.price = str(post.price_new) if post.price_new is not None else ''
        post.save(update_fields=['price'])


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_post_is_available'),
    ]

    operations = [
        migrations.RunPython(copy_price_forward, copy_price_backward),
    ]
