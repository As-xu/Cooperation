from django.apps import AppConfig
from django.shortcuts import redirect

class CoopuserConfig(AppConfig):
    name = 'coopuser'


def login_judge(view_func):
    def judge(request, *args, **kwargs):
        if request.COOKIES.get("id", "") == "":
            return redirect("/user/login")
        res = view_func(request, *args, **kwargs)
        return res
    return judge

