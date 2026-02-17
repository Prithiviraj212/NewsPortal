from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from newsapp.models import CustomUser, News, Category, Page, Comments, Subcategory, Contact

User = get_user_model()

# ------------------ Base Pages ------------------
def BASE(request):
    return render(request, 'base.html')


def BASE1(request):
    return render(request, 'base1.html')


# ------------------ Home Page ------------------
def INDEX(request):
    postnews = News.objects.order_by('-posted_date')[:3]
    postnews1 = News.objects.order_by('-posted_date')[:4]
    category = Category.objects.all()[:4]
    recentnews = News.objects.order_by('-posted_date')[:5]

    context = {
        'postnews': postnews,
        'category': category,
        'recentnews': recentnews,
        'postnews1': postnews1
    }

    return render(request, 'home.html', context)


# ------------------ Static Pages ------------------
def ABOUTUS(request):
    first_page = Page.objects.first()
    return render(request, 'aboutus.html', {'page': first_page})


def CONTACTUS(request):
    first_page = Page.objects.first()
    return render(request, 'contactus.html', {'page': first_page})


# ------------------ Contact Form Submit ------------------
def contact_submit(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if name and email and message:
            Contact.objects.create(
                name=name,
                email=email,
                message=message,
                posted_date=timezone.now()
            )
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contactus')
        else:
            messages.error(request, "Please fill all fields!")
            return redirect('contactus')

    return redirect('contactus')


# ------------------ Category Page ------------------
def category_detail(request, id):
    catid = get_object_or_404(Category, id=id)
    news_list = News.objects.filter(cat_id=catid).order_by('-posted_date')

    paginator = Paginator(news_list, 4)
    page_number = request.GET.get('page')
    news = paginator.get_page(page_number)

    context = {
        'catid': catid,
        'news': news
    }

    return render(request, 'categorywise_newsdetail.html', context)


# ------------------ Single News Page ------------------
def VIEW_SINGLENEWS(request, id):
    sinnews = get_object_or_404(News, id=id)
    recentnews = News.objects.order_by('-posted_date')[:4]
    category_counts = Category.objects.annotate(news_count=Count('news'))
    comments_list = Comments.objects.filter(news_id=sinnews, status='Approved')

    if request.method == "POST":
        comment = request.POST.get('comment')
        name = request.POST.get('name')
        email = request.POST.get('email')

        if comment and name and email:
            Comments.objects.create(
                news_id=sinnews,
                comment=comment,
                name=name,
                email=email,
            )
            return redirect('thank_you')

    context = {
        'sinnews': sinnews,
        'recentnews': recentnews,
        'category_counts': category_counts,
        'comments_list': comments_list,
    }

    return render(request, 'single-news-details.html', context)


# ------------------ Thank You Page ------------------
def THANKYOU(request):
    return render(request, 'thankyou.html')


# ------------------ Admin Dashboard ------------------
@login_required(login_url='login')
def DASHBOARD(request):
    category_count = Category.objects.count()
    subcategory_count = Subcategory.objects.count()
    news_count = News.objects.count()
    subadmin_count = CustomUser.objects.filter(user_type=2).count()
    recent_news = News.objects.order_by('-posted_date')[:5]

    context = {
        'category_count': category_count,
        'subcategory_count': subcategory_count,
        'news_count': news_count,
        'subadmin_count': subadmin_count,
        'recent_news': recent_news,
    }

    return render(request, 'dashboard.html', context)


# ------------------ Login ------------------
def LOGIN(request):
    return render(request, 'login.html')


def doLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if remember_me:
                request.session.set_expiry(2592000)  # 30 days
            else:
                request.session.set_expiry(0)

            if str(user.user_type) in ['1', '2']:
                return redirect('dashboard')
        else:
            messages.error(request, 'Username or Password is not valid')
            return redirect('login')

    return redirect('login')


def doLogout(request):
    logout(request)
    return redirect('login')


# ------------------ Admin Profile ------------------
@login_required(login_url='login')
def ADMIN_PROFILE(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(request, 'profile.html', {'user': user})


@login_required(login_url='login')
def ADMIN_PROFILE_UPDATE(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        customuser = CustomUser.objects.get(id=request.user.id)
        customuser.first_name = first_name
        customuser.last_name = last_name

        if profile_pic:
            customuser.profile_pic = profile_pic

        customuser.save()
        messages.success(request, "Profile updated successfully")
        return redirect('admin_profile')

    return redirect('admin_profile')


@login_required(login_url='login')
def CHANGE_PASSWORD(request):
    if request.method == "POST":
        current = request.POST.get('cpwd')
        new_pwd = request.POST.get('npwd')

        user = User.objects.get(id=request.user.id)
        if user.check_password(current):
            user.set_password(new_pwd)
            user.save()
            login(request, user)
            messages.success(request, 'Password changed successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Current password incorrect!')
            return redirect('change_password')

    return render(request, 'change-password.html')


# ------------------ Search News ------------------
def SEARCH_NEWS(request):
    query = request.GET.get('query', '')

    if query:
        searchnews = News.objects.filter(
            Q(posttitle__icontains=query) |
            Q(cat_id__catname__icontains=query) |
            Q(subcategory_id__subcatname__icontains=query)
        ).order_by('-posted_date')

        paginator = Paginator(searchnews, 10)
        page_number = request.GET.get('page', 1)

        try:
            searchnews_paginated = paginator.page(page_number)
        except PageNotAnInteger:
            searchnews_paginated = paginator.page(1)
        except EmptyPage:
            searchnews_paginated = paginator.page(paginator.num_pages)

        return render(request, 'search-news.html', {
            'searchnews': searchnews_paginated,
            'query': query
        })

    return render(request, 'search-news.html')
