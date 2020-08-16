import uuid

from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from apps.user.models import User
from helpers import functions


class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, null=True, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'slug':self.slug})


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, null=True, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Tag, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:tag', kwargs={'slug':self.slug})


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=144, unique=True)
    slug = models.SlugField(null=True, blank=True, default='', max_length=500)
    body = RichTextUploadingField()
    image = models.ImageField(upload_to=functions.upload_location_blog, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    published = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    date_published = models.DateTimeField(null=True, blank=True, default=functions.return_date_time)
    date_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['date_published']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.body = functions.remove_script_tags(self.body)

        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post', kwargs={'slug':self.slug})

    def is_published(self):
        return self.published

    def get_image_url(self):
        if self.image:
            return self.image.url
        else:
            # TODO: move this field in settings
            return "/static/img/article-5.jpg"
