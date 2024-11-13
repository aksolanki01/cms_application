from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from django.utils.text import slugify
from django.conf import settings


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    profession = models.CharField(max_length=255, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    reset_token = models.CharField(max_length=255, null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)  


    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.name


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    description = models.TextField()
    public = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Like(models.Model):
    like_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} liked {self.post.title}"
