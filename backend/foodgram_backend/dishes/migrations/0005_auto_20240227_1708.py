# Generated by Django 3.2.3 on 2024-02-27 17:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dishes', '0004_auto_20240225_1500'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('image', models.ImageField(blank=True, upload_to='dishes/', verbose_name='Picture')),
                ('cooking_time', models.PositiveSmallIntegerField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField()),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dishes.ingredient')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dishes.recipe')),
            ],
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(through='dishes.RecipeIngredient', to='dishes.Ingredient'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(to='dishes.Tag'),
        ),
    ]