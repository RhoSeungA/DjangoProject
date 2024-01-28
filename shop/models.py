from django.db import models
from django.contrib.auth.models import User
import os
from markdownx.models import MarkdownxField
from django.core.validators import MaxValueValidator, MinValueValidator
from markdownx.utils import markdown

# Create your models here.
class PublishingCompany(models.Model):
    name = models.CharField(max_length=50, unique=True)
    address=models.CharField(max_length=100,unique=True)
    tell = models.CharField(max_length=20,unique=True)
    information = models.TextField()
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return f'/shop/publisher_page/{self.name}/'



class Author(models.Model):
    name = models.CharField(max_length=50, unique=True)
    author_info = models.TextField()
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return f'/shop/author/{self.name}/'
#
class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

class KeyWord(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    def __str__(self):
        return self.name
    def get_objects(self):
        x = Book.objects.filter(keyword=self)
        return x
    def get_4_objects(self):
        x=Book.objects.filter(keyword=self)
        while(len(x)>=4):
            if (len(x) > 4):
                x[4].delete()
        return x
    def get_name(self):
        return self.name
    def get_absolute_url(self):
        return f'/shop/keyword/{self.name}/'



class Book(models.Model):
    title = models.CharField(max_length=30)
    introduction = MarkdownxField()
    head_image = models.ImageField(upload_to='shop/images/', blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    post_writer = models.ForeignKey(User, null=True ,on_delete=models.SET_NULL)
    release_date= models.DateField()
    author=models.ForeignKey(Author, null=True,blank=True ,on_delete=models.SET_NULL)
    price = models.IntegerField()
    sale=models.IntegerField(default=0,null=True,blank=True, validators=[MaxValueValidator(100), MinValueValidator(0)])

    genre = models.ForeignKey(Genre, null=True, blank=True, on_delete=models.SET_NULL)
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.SET_NULL)
    publisher = models.ForeignKey(PublishingCompany, null=True, blank=True, on_delete=models.SET_NULL)
    keyword = models.ManyToManyField(KeyWord, blank=True)

    def get_absolute_url(self):
        return f'/shop/{self.pk}/'

    def get_sale_price(self):
        return (int)(self.price * (1 - (self.sale / 100)))

    def on_sale(self):
        if (self.sale == 0):
            return False
        else:
            return True

    def __str__(self):
        return self.title

    def get_content_markdown(self):
        return markdown(self.introduction)





class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    writer = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at= models.DateTimeField(auto_now=True)
    score=models.IntegerField(default=0,null=True,blank=True, validators=[MaxValueValidator(5), MinValueValidator(1)])
    secret=models.BooleanField(default=False)


    def __str__(self):
        return f'{self.writer} : {self.content}'

    def get_absolute_url(self):
        return f'{self.book.get_absolute_url()}#comment-{self.pk}'
    def get_absolute_comment_url(self):
        return f'{self.book.get_absolute_url()}'

    def get_avatar_url(self):
        if self.writer.socialaccount_set.exists():
            return self.writer.socialaccount_set.first().get_avatar_url()
        else:
            return f'https://dummyimage.com/50x50/ced4da/6c757d.jpg'


class CommentOfComment(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    parent_Comment=models.ForeignKey(Comment, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.writer} : {self.content}'
    def get_absolute_url(self):
        return f'{self.parent_Comment.get_absolute_url()}'


