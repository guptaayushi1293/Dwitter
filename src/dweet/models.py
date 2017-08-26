from __future__ import unicode_literals

from django.db import models
from django.conf import settings
# Create your models here.


class Dweet(models.Model):

    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=140)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, verbose_name="posted by", db_column='user_id', on_delete=models.CASCADE)
    dweeted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "dweets"

    def __str__(self):
        return str(self.id + " - " + self.content)


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, verbose_name="commented by", db_column='user_id', on_delete=models.CASCADE)
    dweet_id = models.ForeignKey(Dweet, db_column='dweet_id', on_delete=models.CASCADE)
    content = models.CharField(max_length=140)
    commented_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "comments"

    def __str__(self):
        return str(self.id + " - " + self.content)


class LikeDweet(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, verbose_name="liked by", db_column='user_id', on_delete=models.CASCADE)
    dweet_id = models.ForeignKey(Dweet, db_column='dweet_id', on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "like_dweet"
        unique_together = ('user_id', 'dweet_id',)

    def __str__(self):
        return str(self.id)


class FollowUser(models.Model):
    id = models.AutoField(primary_key=True)
    followed_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, related_name="followed_by", db_column='followed_by', on_delete=models.CASCADE)
    followed_to = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, related_name="followed_to", db_column='followed_to', on_delete=models.CASCADE)

    class Meta:
        db_table = "follow_user"

    def __str__(self):
        return str(self.id)


