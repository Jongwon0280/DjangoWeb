
import os.path

from django.contrib.auth.models import User
from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdown


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=50, unique=True, allow_unicode=True )


    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}'

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=50, unique=True, allow_unicode=True )


    def get_absolute_url(self):
        return f'/blog/category/{self.slug}'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

class Post(models.Model):
    title = models.CharField(max_length=30)
    hook = MarkdownxField()
    content = MarkdownxField()

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return f'[{self.pk}] {self.title} - {self.author}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)
    def get_content_markdown(self):
        #랜더링한 마크다운 전송
        return markdown(self.content)
    def get_hook_markdown(self):
        #랜더링한 마크다운 전송
        return markdown(self.hook)
#대댓글 기능?
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    content = MarkdownxField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}::{self.content}'

    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}'

    def get_content_markdown(self):
        #랜더링한 마크다운 전송
        return markdown(self.content)




