from django.contrib.auth.models import User
from django.db import models


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.IntegerField(default=0)

    def update_rating(self):
        self.author_rating = sum([comment.comment_rating for comment in self.user.comment_set.all()])
        self.author_rating += sum([post.post_rating * 3 for post in self.post_set.all()])
        self.author_rating += sum(
            [comment.comment_rating for comment in Comment.objects.filter(posts__author=self).exclude(users=self.user)])
        self.save()


class Category(models.Model):
    category = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    article = 'AR'
    news = 'NW'
    POST_NEWS = [
        ('AR', 'Статья'),
        ('NW', 'Новость')
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    article_or_news = models.CharField(choices=POST_NEWS, max_length=2, default=article)
    date_created = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=100)
    text = models.TextField()
    post_rating = models.IntegerField(default=0)

    def post_like(self):
        self.post_rating += 1
        self.save()

    def post_dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        length = 124
        if len(self.text) > length:
            description = self.text[:length]
            for i in range(length, len(self.text)):
                if not self.text[i] == ' ':
                    description += self.text[i]
                else:
                    return description + '...'
        else:
            return self.text
        return description


class PostCategory(models.Model):
    posts = models.ForeignKey(Post, on_delete=models.CASCADE)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    posts = models.ForeignKey(Post, on_delete=models.CASCADE)
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def comment_like(self):
        self.comment_rating = +1
        self.save()

    def comment_dislike(self):
        self.comment_rating = -1
        self.save()
