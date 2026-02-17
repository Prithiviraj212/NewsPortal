from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Category, Subcategory, News, Page, Comments, CustomUser
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# ------------------ BASE TEMPLATES ------------------
def BASE(request):
    return render(request, 'base.html')

def BASE1(request):
    return render(request, 'base1.html')


# ------------------ HOME PAGE ------------------
def INDEX(request):
    latest_news = News.objects.filter(status='Published').order_by('-posted_date')[:10]
    return render(request, 'index.html', {'latest_news': latest_news})


# ------------------ STATIC PAGES ------------------
def ABOUTUS(request):
    page = Page.objects.first()
    return render(request, 'aboutus.html', {'page': page})

def CONTACTUS(request):
    return render(request, 'contactus.html')


# ------------------ CATEGORY PAGE ------------------
def category_detail(request, id):
    category = Category.objects.get(id=id)
    news_list = News.objects.filter(cat_id=category, status='Published').order_by('-posted_date')
    return render(request, 'category_detail.html', {'category': category, 'news_list': news_list})


# ------------------ SINGLE NEWS PAGE ------------------
def VIEW_SINGLENEWS(request, id):
    news = News.objects.get(id=id)
    comments = Comments.objects.filter(news_id=news, status='Approved').order_by('-posted_date')
    return render(request, 'view_single_news.html', {'news': news, 'comments': comments})


# ------------------ THANK YOU PAGE ------------------
def THANKYOU(request):
    return render(request, 'thank_you.html')


# ------------------ SEARCH NEWS ------------------
def SEARCH_NEWS(request):
    query = request.GET.get('q')
    results = News.objects.filter(posttitle__icontains=query, status='Published') if query else []
    return render(request, 'search_news.html', {'results': results, 'query': query})


# ------------------ AUTH ------------------
def LOGIN(request):
    return render(request, 'login.html')

def doLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.user_type == '1':  # admin
                return redirect('dashboard')
            else:
                return redirect('index')
        else:
            messages.error(request, 'Invalid Username or Password')
            return redirect('login')
    return redirect('login')


@login_required(login_url='login')
def doLogout(request):
    logout(request)
    return redirect('login')


# ------------------ ADMIN DASHBOARD ------------------
@login_required(login_url='login')
def DASHBOARD(request):
    total_news = News.objects.count()
    total_categories = Category.objects.count()
    return render(request, 'dashboard.html', {'total_news': total_news, 'total_categories': total_categories})


@login_required(login_url='login')
def ADMIN_PROFILE(request):
    return render(request, 'admin_profile.html')


@login_required(login_url='login')
def ADMIN_PROFILE_UPDATE(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        if request.FILES.get('profile_pic'):
            user.profile_pic = request.FILES['profile_pic']
        user.save()
        messages.success(request, 'Profile updated successfully')
        return redirect('admin_profile')
    return redirect('admin_profile')


@login_required(login_url='login')
def CHANGE_PASSWORD(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        user = request.user
        if not user.check_password(current_password):
            messages.error(request, 'Current password is incorrect')
        elif new_password != confirm_password:
            messages.error(request, 'New password and confirm password do not match')
        else:
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password changed successfully')
            return redirect('login')
    return render(request, 'change_password.html')
