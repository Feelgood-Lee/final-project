from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from .forms import LoginForm, RegisterForm
from .models import User
from django.core.paginator import Paginator
from django.http.response import JsonResponse

User = get_user_model()


def index(request):
    user = User.objects.filter(id=request.user.id).first()
    return render(request, "base.html")

@csrf_exempt
def get_user(request, user_id):
    print(user_id)
    if request.method == "GET":
        abc = request.GET.get("abc")
        xyz = request.GET.get("xyz")
        user = User.objects.filter(pk=user_id).first()
        return render(request, "base.html", {"user": user, "params": [abc, xyz]})
    elif request.method == "POST":
        username = request.GET.get("username")
        if username:
            user = User.objects.filter(pk=user_id).update(username=username)

        return JsonResponse(dict(msg="You just reached with Post Method!"))

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/login")
    else:
        logout(request)
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method =="POST":
        form = LoginForm(request.POST)                             
        if form.is_valid():                                        
            username= form.cleaned_data.get("username")
            raw_password=form.cleaned_data.get("password")
            msg = "올바른 유저ID와 패스워드를 입력하세요."
#            request.session['user'] = form.username                 
#            return redirect('/')
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                msg = "등록된 사용자가 없습니다."
            else:
                if user.check_password(raw_password):
                    msg = None
                    login(request, user)
                    return render(request, 'index.html')
    else:
        msg = None
        form = LoginForm()                                         
    
    return render(request, 'login.html', {'form':form, "msg":msg})   
    #return render(request, 'index.html', {'form':form, "msg":msg})          

def logout_view(request):
    logout(request)
    return redirect("index")


# TODO: 8. user 목록은 로그인 유저만 접근 가능하게 해주세요
#def user_list_view(request):
    # TODO: 7. /users 에 user 목록을 출력해주세요
    # TODO: 9. user 목록은 pagination이 되게 해주세요
    #return render(request, "users.html", {"users": users})

@login_required
def user_list_view(request):
    page = int(request.GET.get("p", 1))
    users = User.objects.all().order_by("-id")
    paginator = Paginator(users, 10)
    users = paginator.get_page(page)

    return render(request, "users.html", {"users": users})
