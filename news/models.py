from datetime import datetime, timezone
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from string import Template


class Author(models.Model):
    user_rate = models.IntegerField(default=0)
    author = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        sum_rating = self.post_set.aggregate(post_rating=Sum('post_rate'))
        result_sum_rating = 0
        try:
            result_sum_rating += sum_rating.get('post_rating')
        except TypeError:
            result_sum_rating = 0

        sum_comment_rating = self.author.comment_set.aggregate(comment_rating=Sum('comment_rate'))
        result_sum_comment_rating = 0
        result_sum_comment_rating += sum_comment_rating.get('comment_rating')

        self.user_rate = result_sum_rating * 3 + result_sum_comment_rating
        self.save()


class Category(models.Model):
    article_category = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.article_category


class Post(models.Model):
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_category = models.ManyToManyField(Category)

    article = 'A'
    news = 'N'

    POSITIONS = [
        (article, "Статья"),
        (news, "Новость"),
    ]

    category = models.CharField(max_length=1,
                                choices=POSITIONS,
                                default=article)

    date_created = models.DateTimeField(auto_now_add=True)

    title = models.CharField(max_length=128)

    content = models.TextField()

    post_rate = models.IntegerField(default=0)
    template_string = "$text..."

    def like(self):
        self.post_rate += 1
        self.save()

    def dislike(self):
        self.post_rate -= 1
        self.save()

    def preview(self):
        return Template(self.template_string).substitute(text=self.content[0:123])

    def __str__(self):
        return f"{self.title} {self.date_created}: {self.content[:20]}..."


class PostCategory(models.Model):
    post_category = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback_text = models.TextField()
    comment_date_created = models.DateTimeField(auto_now_add=True)
    comment_rate = models.IntegerField(default=0)

    def like(self):
        self.comment_rate += 1
        self.save()

    def dislike(self):
        self.comment_rate -= 1

    def __str__(self):
        return f'{self.comment_post.title}: {self.comment_user.username}: {self.feedback_text[:20]}... {self.comment_date_created}'

