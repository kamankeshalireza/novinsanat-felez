from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_available',
            field=models.BooleanField(default=True, verbose_name='موجود است؟'),
        ),
        migrations.AddField(
            model_name='post',
            name='price_new',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='قیمت (تومان)'),
        ),
    ]
