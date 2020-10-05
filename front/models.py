from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify


def replace_characters(text):
    text = text.replace('ə', 'e')
    text = text.replace('ç', 'c')
    text = text.replace('ğ', 'g')
    text = text.replace('ö', 'o')
    text = text.replace('ş', 's')
    text = text.replace('ü', 'u')

    return text


def generate_slug(name, model):
    name = replace_characters(name)
    slug = slugify(name)
    num = 1
    while model.objects.filter(slug=slug).exists():
        slug = '{}-{}'.format(slug, num)
        num += 1
    return slug


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=180)
    is_published_menu = models.BooleanField(default=False)
    is_published_right = models.BooleanField(default=True)
    slug = models.CharField(max_length=180, unique=True, blank=True)


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slug(self.name, Category)
        super().save()


class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    picture = models.ImageField(upload_to='posts/', default=None, null=True, blank=True)
    author = models.CharField(max_length=50)
    title = models.CharField(max_length=100, null=True)
    content = models.TextField()
    time = models.DateTimeField(default=None, null=True)
    is_deleted = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    slug = models.CharField(max_length=180, unique=True, blank=True)


    def __str__(self):
        return self.author

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slug(self.title, Post)
        super().save()



class SocialAccounts(models.Model):
    icon_name =models.CharField(max_length=50)
    url = models.URLField(max_length=100)

    def __str__(self):
        return self.icon_name


class Comment(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=70)
    time = models.DateTimeField(default=None, null=True)
    contain = models.CharField(max_length=200)

    def __str__(self):
        return self.name