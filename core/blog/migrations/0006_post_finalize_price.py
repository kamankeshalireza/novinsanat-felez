from django.core.validators import MinValueValidator
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_post_migrate_price_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='price',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='price_new',
            new_name='price',
        ),
        migrations.AlterField(
            model_name='post',
            name='price',
            field=models.PositiveIntegerField(
                blank=True,
                null=True,
                validators=[MinValueValidator(0)],
                verbose_name='قیمت (تومان)',
                help_text='اگر خالی بگذارید، به‌جای عدد «استعلام قیمت» نمایش داده می‌شود.',
            ),
        ),
    ]
