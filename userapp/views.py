from django.shortcuts import render, reverse
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from .models import BlogUser
from random import Random
from django.core.mail import send_mail
from .models import EmailVerifyRecord
from django.conf import settings
# Create your views here.
# 登录
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 查找传的数据是否跟数据库里的一样
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('blog:index'))
            else:
                return render(request, 'login.html', {'error_msg': '用户未激活'})

        else:
            return render(request, 'login.html', {'error_msg': '用户名或者密码错误'})


# 注销
class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('blog:index'))


# 注册
class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')
    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        user = BlogUser()
        user.username = username
        user.password = make_password(password)
        user.email = email
        user.is_active = True

        user.save()
        return render(request,'login.html')

#生成随机字符串  注册验证
def make_random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0,length)]
    return str

#发送邮件
def my_send_email(email,send_type='register'):
    pass
