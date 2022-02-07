from news.models import Comment, Post, Author, Category, PostCategory
from django.contrib.auth.models import User

best_article=Post.objects.all().order_by('-post_rating')[0]
