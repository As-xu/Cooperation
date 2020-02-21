from django.db import models


class CoopUserInfo(models.Model):
    nickname = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    gender = models.NullBooleanField(default=1)
    school = models.CharField(max_length=50, default="")
    hobby = models.CharField(max_length=200, blank=True)
    qqNum = models.CharField(max_length=10, default="", blank=True)
    phone = models.CharField(max_length=11)
    profession = models.CharField(max_length=50)
    createTime = models.DateField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.nickname)

    def set_nickname(self, value):
        self.nickname = value

    def set_age(self, value):
        self.age = value

    def set_gender(self, value):
        self.gender = value

    def set_school(self, value):
        self.school = value

    def set_hobby(self, value):
        self.nickname = value

    def set_qqNum(self, value):
        self.nickname = value

    def set_phone(self, value):
        self.phone = value

    def set_profession(self, value):
        self.profession = value

class CoopPost(models.Model):
    postTitle = models.CharField(max_length=100)
    postWish = models.NullBooleanField()
    postMaster = models.ForeignKey('CoopUserInfo', on_delete=models.DO_NOTHING)
    postTag = models.ForeignKey('CoopTag', on_delete=models.DO_NOTHING)
    postContent = models.CharField(max_length=300)
    postCreateTime = models.DateField(auto_now_add=True)
    isDelete = models.NullBooleanField(default=False)

    def __str__(self):
        return "{}".format(self.postTitle)


class CoopComment(models.Model):
    commentPost = models.ForeignKey('CoopPost', on_delete=models.DO_NOTHING)
    commentUser = models.ForeignKey('CoopUserInfo', on_delete=models.DO_NOTHING)
    commentContent = models.CharField(max_length=200)
    commentCreateTime = models.DateTimeField(auto_now_add=True)
    commentUp = models.ForeignKey('self', on_delete=models.DO_NOTHING, blank=True, null=True)
    isDelete = models.NullBooleanField(default=False)

    def __str__(self):
        return "{}".format(self.commentContent)


class CoopTag(models.Model):
    tagName = models.CharField(max_length=20)
    isDelete = models.NullBooleanField(default=False)

    def __str__(self):
        return "{}".format(self.tagName)



# class CoopUserTeam(models.Model):
#     pass
# python manage.py makemigrations
# python manage.py migrate﻿​

