from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path("user/login", views.login),
    path("user/register", views.register),
    path("user/login_handle", views.login_handle),
    path("user/register_handle", views.register_handle),
    path("user/logout", views.logout),

    path("user/userPostList", views.post_user_list),
    path("user/userInfo", views.user_info),
    path("user/infoSet", views.user_info_set),

    path("project", views.posts_project),
    path("projectTag", views.posts_project_filter),
    path("cooperation", views.post_coop),
    path("cooperationTag", views.post_coop_filter),

    # path("postDetail", views.post_detail),
    path("post/<int:num>", views.post_detail),
    path("addComment", views.add_comment),
    path("addPost", views.add_post),
    path("addPostHandle", views.add_post_handle),
    path("getTag", views.getTag),
]
