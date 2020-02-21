from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from .models import *
from .apps import login_judge
from django.db.models import Q
import json
import re


# 使用json对象来存储cookie的值,避免中文问题,
# Create your views here.


def index(request):
    """
    首页
    """
    isLogin = request.session.get("username", "")
    user_id = request.session.get("id", "")

    if isLogin == "":
        content = {
            "isLogin": False,
            "username": isLogin,
        }
    else:
        content = {
            "isLogin": True,
            "username": isLogin,
        }
    response = render(request, "coopuser/index.html", content)
    # 用户名转为json对象,避免中文问题
    response.set_cookie("username", json.dumps(isLogin))
    response.set_cookie("id", user_id)
    return response


def logout(request):
    """
    注销
    :param request:
    :return:
    """
    request.session.flush()
    return redirect("/")


def login(request):
    """
    登录
    :param request:
    :return:
    """

    return render(request, "coopuser/login.html", {
        "phoneError": False,
        "passwordError": False,
    })


def login_handle(request):
    """
    登录处理
    :param request:
    :return:
    """

    user = CoopUserInfo.objects.filter(phone=request.POST["phone"])
    if len(user) == 1:
        # print(user)
        if user[0].password == request.POST["pword"]:
            request.session["username"] = user[0].nickname
            request.session["id"] = user[0].id
            # print(user[0].nickname)
            # print(user[0].id)

            return redirect("/")
        else:
            return render(request, "coopuser/login.html", {
                "phoneError": False,
                "passwordError": True,
            })
    else:
        return render(request, "coopuser/login.html", {
            "phoneError": True,
            "passwordError": False,
        })


def register(request):
    """
    注册
    :param request:
    :return:
    """
    content = {
        "name": True,
        "password": True,
        "age": True,
        "gender": True,
        "school": True,
        "hobby": True,
        "phone": True,
        "qqNum": True,
        "profession": True
    }
    return render(request, "coopuser/register.html", content)


def register_handle(request):
    """
    注册处理
    :param request:
    :return:
    """
    content = userinfo_check(request)

    for flag in content.values():
        # print(flag)
        if flag is False:
            return render(request, "coopuser/register.html", content)

    userInfo = CoopUserInfo.objects.create(
        nickname=request.POST["Name"],
        password=request.POST["pwd"],
        age=request.POST["age"],
        gender=request.POST["gender"],
        school=request.POST["school"],
        hobby=request.POST["hobby"],
        phone=request.POST["phone"],
        qqNum=request.POST["qqNumber"],
        profession=request.POST["profession"],
    )
    userInfo.save()
    return redirect("/user/login")


@login_judge
def user_info(request):
    """
    用户信息
    :param request:
    :return:
    """
    userInfo = CoopUserInfo.objects.get(pk=request.COOKIES["id"])
    content = {
        "info": {
            "name": ("昵称", userInfo.nickname),
            "age": ("年龄", userInfo.age),
            "gender": ("性别", (lambda x: "男" if x is True else "女")(userInfo.gender)),
            "school": ("学校", userInfo.school),
            "hobby": ("爱好", userInfo.hobby),
            "qqNum": ("QQ号", userInfo.qqNum),
            "phone": ("手机号", userInfo.phone),
            "profession": ("专业", userInfo.profession),
        },
        "page": 0,
    }
    return render(request, "coopuser/userInfo.html", content)


@login_judge
def user_info_set(request):
    """
    用户信息更改
    :param request:
    :return:
    """
    userInfo = CoopUserInfo.objects.get(pk=request.COOKIES["id"])
    attr_maps = {
        "name": name_check,
            # userInfo.nickname,
        "age": [age_check, userInfo.set_age],
        "gender": [gender_check, userInfo.set_gender],
        "school": [school_check,userInfo.set_school],
        "hobby": [hobby_check, userInfo.set_hobby],
        "qqNum": [qqNum_check, userInfo.set_qqNum],
        "phone": [phone_check, userInfo.set_phone],
        "profession": [profession_check, userInfo.set_profession],
    }

    info_check(attr_maps[request.GET.get("attr")][0], request.GET.get("value"))

    attr_maps[request.GET.get("attr")][1](request.GET.get("value"))

    print(request.GET.get("attr"))
    print(request.GET.get("value"))
    userInfo.save()
    return JsonResponse({
        "state": 1,
        request.GET.get("attr"): request.GET.get("value")
    })
    


@login_judge
def post_user_list(request):
    """
    用户帖子列表
    :param request:
    :return:
    """
    user_posts = CoopPost.objects.filter(postMaster_id=request.COOKIES["id"])
    res_post = []
    for post in user_posts:
        res_post.append((post.id, post.postTitle, post.postContent))
    content = {
        "info": res_post,
        "page": 1,
    }
    return render(request, "coopuser/userInfo.html", content)


def posts_project(request):
    """
    返回项目贴
    :param request:
    :return:
    """
    posts = CoopPost.objects.filter(Q(isDelete=False)&Q(postWish=True))

    tag_posts = []

    for tag in CoopTag.objects.filter(isDelete=False):
        tag_posts.append((posts.filter(postTag=tag.id).count(), tag.tagName))


    return render(request, "coopuser/postList.html", {
        "posts": posts,
        "tag": tag_posts,
        "type": 0,
    })


def posts_project_filter(request):
    """
    返回标签项目贴
    :param request:
    :return:
     & Q(postTag__tagName__exact=request.GET.get("tag"))
    """
    posts = list(CoopPost.objects.filter(Q(isDelete=False) & Q(postWish=True)& Q(postTag__tagName__exact=request.GET.get("tag"))).values(
        "id", "postTitle", "postMaster__nickname", "postTag__tagName", "postContent", "postCreateTime",))
    print(posts)
    print(request.GET.get("tag", ""))
    return JsonResponse({
        "posts": list(posts)
    })

def post_coop(request):
    """
    返回合作贴
    :param request:
    :return:
    """
    posts = CoopPost.objects.filter(Q(isDelete=False) & Q(postWish=False))

    tag_posts = []

    for tag in CoopTag.objects.filter(isDelete=False):
        tag_posts.append((posts.filter(postTag=tag.id).count(), tag.tagName))

    return render(request, "coopuser/postList.html", {
        "posts": posts,
        "tag": tag_posts,
        "type": 1,
    })



def post_coop_filter(request):
    """
    返回标签合作贴
    :param request:
    :return:
    """
    posts = list(CoopPost.objects.filter(Q(isDelete=False) & Q(postWish=False) & Q(postTag__tagName__exact=request.GET.get("tag"))).values(
        "id", "postTitle", "postMaster__nickname", "postTag__tagName", "postContent", "postCreateTime"))
    return JsonResponse({
        "posts":posts
    })




def post_detail(request, num=0):
    """
    返回帖子详情
    :param num:
    :param request:
    :return:
    """
    if num <= 0:
        raise Http404("error")
    try:
        post = CoopPost.objects.get(pk=num)
        comment = CoopComment.objects.filter(commentPost_id=num).order_by("id")
        user = CoopUserInfo.objects.get(cooppost=num)
    except CoopPost.DoesNotExist:
        raise Http404("error")
    except CoopPost.MultipleObjectsReturned:
        raise Http404("error")
    else:
        return render(request, "coopuser/postDetail.html", context={
            "post": post,
            "comment": comment,
            "user": user,
        })


@login_judge
def add_post(request):
    """
    添加帖子
    :param request:
    :return:
    """
    content = {
        "title": True,
        "Content": True
    }
    return render(request, "coopuser/addPost.html", content)


def add_post_handle(request):
    content = post_check(request)
    for i in content.values():
        if i is False:
            print(content)
            print(i)
            print(11111)
            return render(request, "coopuser/addPost.html", content)

    post_ob = CoopPost.objects.create(
        postTitle=request.POST.get("postTitle", ""),
        postWish=request.POST.get("wish", ""),
        postContent=request.POST.get("postContent", ""),
        postMaster=content["id"],
        postTag=content["tag"]
    )
    post_ob.save()
    return redirect("/user/userPostList")


@login_judge
def add_comment(request):
    """
    添加留言
    :param request:
    :return:
    """
    post_num = request.GET.get("page", "")
    if post_num == "":
        return HttpResponse("over")
    post_ob = CoopPost.objects.get(id=post_num)
    last_comment_obs = CoopComment.objects.filter(commentPost_id=post_num).order_by("commentCreateTime")
    if last_comment_obs.exists():
        last_comment_ob = last_comment_obs[0]
    else:
        last_comment_ob = None
    user_num = request.COOKIES.get("id")
    user_ob = CoopUserInfo.objects.get(id=user_num)
    comment = request.GET.get("comment", "")

    CoopComment.objects.create(
        commentPost=post_ob,
        commentUser=user_ob,
        commentContent=comment,
        commentUp=last_comment_ob
    )
    # print(post_num)
    # print(post_ob)
    # print(last_comment_ob)
    # print(user_ob)
    # print(comment)
    return redirect("post/"+post_num)



def getTag(request):
    """
    ajax请求数据
    :param request:
    :return:
    """
    tag_dict = {}
    for tag in CoopTag.objects.all():
        tag_dict[tag.id] = tag.tagName
    return JsonResponse(tag_dict)


#
# 信息修改的字段检查函数
def info_check(check, value):
    if check(value):
        return False


# 下面都是注册字段检查函数
def name_check(name):
    # name = str(name)
    if len(name) > 20 or len(name) < 1:
        return False
    elif name.isspace() or name.isdigit():
        return False
    else:
        if re.search("[*&%()[]!`~", name) is None:
            return True
        return False


def pwd_check(pwd):
    # pwd = str(pwd)
    if len(pwd) > 20 or len(pwd) < 6:
        return False
    else:
        if re.search("\s", pwd) is None:
            return True
        return False


def age_check(age):
    # age = str(age)
    if age.isdigit():
        if int(age) >= 255 or int(age) <= 0:
            return False
        return True
    return False

def gender_check(gender):
    if gender == "男":
        return True
    elif gender == "女":
        return False
    return None

def school_check(school):
    if len(school) <= 50:
        return True
    return False


def hobby_check(hobby):
    if len(hobby) <= 200:
        return True
    return False


def qqNum_check(qqNum):
    if qqNum.isdigit:
        if len(qqNum) <= 10 or len(qqNum) >= 5:
            return True
        return False
    return False


def phone_check(phone):
    if phone.isdigit:
        if len(phone) == 11:
            return True
        return False
    return False


def profession_check(profession):
    if len(profession) <= 50:
        return True
    return False


def userinfo_check(request):
    content = {
        "name": name_check(request.POST["Name"]),
        "password": pwd_check(request.POST["pwd"]),
        "age": age_check(request.POST["age"]),
        "gender": True,
        "school": school_check(request.POST["school"]),
        "hobby": hobby_check(request.POST["hobby"]),
        "phone": phone_check(request.POST["phone"]),
        "qqNum": qqNum_check(request.POST["qqNumber"]),
        "profession": profession_check(request.POST["profession"]),
    }
    return content


#添加帖子的字段检查函数

def title_check(title):
    if (len(title) >= 100) or (title == ""):
        print("11111")
        print(title)
        print(len(title))
        return False
    return True

def content_check(content):
    if (len(content) >= 300) or (content == ""):
        print(len(content))
        return False
    return True

def id_check(id):
    if id == "":
        return False
    else:
        try:
            user_ob = CoopUserInfo.objects.get(pk=id)
        except CoopPost.DoesNotExist:
            return False
        except CoopPost.MultipleObjectsReturned:
            return False
        else:
            return user_ob


def tag_check(tag):
    if tag == "":
        return False
    return CoopTag.objects.get(id=tag)


def post_check(request):
    content = {
        "title": title_check(request.POST.get("postTitle")),
        "content": content_check(request.POST.get("postContent")),
        "id": id_check(request.COOKIES["id"]),
        "tag": tag_check(request.POST.get("postTag", "")),
    }
    return content


