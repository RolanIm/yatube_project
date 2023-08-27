from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class Group(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(
        verbose_name='Title of the text',
        help_text='Enter the title',
        max_length=100,
        blank=True,
        null=True
    )
    text = models.TextField(
        verbose_name='Text of the post',
        help_text="Enter text of the post"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Author'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name='posts',
        blank=True,
        null=True,
        verbose_name='Group',
        help_text='Choice group'
    )
    pub_date = models.DateTimeField(
        verbose_name='Publication date',
        auto_now_add=True,
        db_index=True
    )
    image = models.ImageField(
        'Image',
        upload_to='posts/',
        blank=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def get_absolute_url(self):
        return reverse('posts:post_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.CharField(max_length=550, verbose_name='Comment')
    created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('posts:post_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.text
