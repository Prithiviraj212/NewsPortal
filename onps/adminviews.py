from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from newsapp.models import CustomUser, Category, Subcategory, News, Page, Comments

# =====================================
# ========== SUBADMIN MANAGEMENT ======
# =====================================

@login_required(login_url='/')
def ADD_SUBADMIN(request):
    if request.method == "POST":
        pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request,'Email already exists')
            return redirect('add_subadmin')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request,'Username already exists')
            return redirect('add_subadmin')
        user = CustomUser(
           first_name=first_name,
           last_name=last_name,
           username=username,
           email=email,
           user_type=2,  # subadmin type
           profile_pic=pic,
        )
        user.set_password(password)
        user.save()            
        messages.success(request,'Sub admin added Successfully')
        return redirect('add_subadmin')
    
    return render(request,'admin/add-subadmin.html')


@login_required(login_url='/')
def MANAGE_SUBADMIN(request):
    subadmin_list = CustomUser.objects.filter(user_type=2)
    paginator = Paginator(subadmin_list, 10)
    page_number = request.GET.get('page')
    try:
        subadmin = paginator.page(page_number)
    except PageNotAnInteger:
        subadmin = paginator.page(1)
    except EmptyPage:
        subadmin = paginator.page(paginator.num_pages)
    
    return render(request,'admin/manage-subadmin.html',{'subadmin': subadmin})


@login_required(login_url='/')
def DELETE_SUBADMIN(request, id):
    subadmin = get_object_or_404(CustomUser, id=id)
    subadmin.delete()
    messages.success(request,'Record Deleted Successfully!')
    return redirect('manage_subadmin')


@login_required(login_url='/')
def VIEW_SUBADMIN(request, id):
    user1 = get_object_or_404(CustomUser, id=id, user_type=2)
    return render(request,'admin/subadmin-profile.html',{"user1": user1})


@login_required(login_url='/')
def SUBADMIN_PROFILE_UPDATE(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        userid = request.POST.get('userid')

        try:
            user = CustomUser.objects.get(id=userid, user_type=2)
            user.first_name = first_name
            user.last_name = last_name
            if profile_pic:
                user.profile_pic = profile_pic
            user.save()
            messages.success(request, "Profile updated successfully")
            return redirect('view_subadmin', id=user.id)
        except CustomUser.DoesNotExist:
            messages.error(request, "User not found.")
        except Exception as e:
            print(e)
            messages.error(request, "Profile update failed.")

    userid = request.GET.get('id')
    user1 = get_object_or_404(CustomUser, id=userid, user_type=2)
    return render(request, 'admin/subadmin-profile.html', {"user1": user1})

# =====================================
# ========== CATEGORY MANAGEMENT =====
# =====================================

@login_required(login_url='/')
def ADD_CATEGORY(request):
    if request.method == "POST":
        catname = request.POST.get('catname')
        catdes = request.POST.get('catdes')
        Category(catname=catname, catdes=catdes).save()
        messages.success(request,'Category added Successfully!')
        return redirect("add_category")
    return render(request,'admin/add_category.html')


@login_required(login_url='/')
def MANAGE_CATEGORY(request):
    cat_list = Category.objects.all()
    paginator = Paginator(cat_list, 10)
    page_number = request.GET.get('page')
    try:
        categories = paginator.page(page_number)
    except PageNotAnInteger:
        categories = paginator.page(1)
    except EmptyPage:
        categories = paginator.page(paginator.num_pages)
    return render(request, 'admin/manage_category.html', {'categories': categories})


@login_required(login_url='/')
def DELETE_CATEGORY(request, id):
    get_object_or_404(Category, id=id).delete()
    messages.success(request,'Record Deleted Successfully!')
    return redirect('manage_category')


@login_required(login_url='/')
def UPDATE_CATEGORY(request, id):
    category = get_object_or_404(Category, id=id)
    return render(request,'admin/update_category.html', {'category': category})


@login_required(login_url='/')
def UPDATE_CATEGORY_DETAILS(request):
    if request.method == 'POST':
        cat = get_object_or_404(Category, id=request.POST.get('cat_id'))
        cat.catname = request.POST.get('catname')
        cat.catdes = request.POST.get('catdes')
        cat.save()
        messages.success(request,"Category updated Successfully!")
        return redirect('manage_category')
    return redirect('manage_category')

# =====================================
# ========== SUBCATEGORY MANAGEMENT ===
# =====================================

@login_required(login_url='/')
def ADD_SUBCATEGORY(request):
    categories = Category.objects.all()
    if request.method == "POST":
        cat = get_object_or_404(Category, id=request.POST.get('cat_id'))
        subcatname = request.POST.get('subcatname')
        Subcategory(cat_id=cat, subcatname=subcatname).save()
        messages.success(request, 'Subcategory Added Successfully!')
        return redirect("add_subcategory")
    return render(request,'admin/add_subcategory.html', {'category': categories})


@login_required(login_url='/')
def MANAGE_SUBCATEGORY(request):
    subcat_list = Subcategory.objects.all()
    paginator = Paginator(subcat_list, 10)
    page_number = request.GET.get('page')
    try:
        subcategories = paginator.page(page_number)
    except PageNotAnInteger:
        subcategories = paginator.page(1)
    except EmptyPage:
        subcategories = paginator.page(paginator.num_pages)
    return render(request, 'admin/manage_subcategory.html', {'subcategories': subcategories})


@login_required(login_url='/')
def DELETE_SUBCATEGORY(request, id):
    get_object_or_404(Subcategory, id=id).delete()
    messages.success(request,'Record Deleted Successfully!')
    return redirect('manage_subcategory')


@login_required(login_url='/')
def UPDATE_SUBCATEGORY(request, id):
    category = Category.objects.all()
    subcategory = get_object_or_404(Subcategory, id=id)
    return render(request,'admin/update_subcategory.html', {'subcategory': subcategory, 'category': category})


@login_required(login_url='/')
def UPDATE_SUBCATEGORY_DETAILS(request):
    if request.method == 'POST':
        subcat = get_object_or_404(Subcategory, id=request.POST.get('subcat_id'))
        subcat.cat_id = get_object_or_404(Category, id=request.POST.get('cat_id'))
        subcat.subcatname = request.POST.get('subcatname')
        subcat.save()
        messages.success(request,"Subcategory updated Successfully!")
        return redirect('manage_subcategory')
    return redirect('manage_subcategory')


@login_required(login_url='/')
def get_subcat(request):
    c_id = request.GET.get('c_id')
    subcat_list = Subcategory.objects.filter(cat_id=c_id)
    html = ''.join([f'<option value="{s.id}">{s.subcatname}</option>' for s in subcat_list])
    return JsonResponse({'subcat_options': html})


# =====================================
# ========== NEWS POSTS MANAGEMENT =====
# =====================================

@login_required(login_url='/')
def ADD_POST(request):
    categories = Category.objects.all()
    if request.method == "POST":
        cat = get_object_or_404(Category, id=request.POST.get('cat_id'))
        subcat = get_object_or_404(Subcategory, id=request.POST.get('subcategory_id'))
        News(
            cat_id=cat,
            subcategory_id=subcat,
            posttitle=request.POST.get('posttitle'),
            postdetails=request.POST.get('postdetails'),
            status=request.POST.get('status'),
            postimage=request.FILES.get('postimage'),
            postedby=request.user.user_type,
            updatedby=request.user.user_type
        ).save()
        messages.success(request, 'News added Successfully!')
        return redirect("add_post")
    return render(request, 'admin/add_postnews.html', {'category': categories})


@login_required(login_url='/')
def MANAGE_POSTS(request):
    post_list = News.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'admin/manage_postnews.html', {'posts': posts})


@login_required(login_url='/')
def DELETE_POSTS(request, id):
    get_object_or_404(News, id=id).delete()
    messages.success(request,'Record Deleted Successfully!')
    return redirect('manage_posts')


@login_required(login_url='/')
def VIEWS_POSTS(request, id):
    post = get_object_or_404(News, id=id)
    categories = Category.objects.all()
    return render(request,'admin/update_news.html',{'postnews': post,'category': categories})


@login_required(login_url='/')
def UPDATE_POST(request):
    if request.method == 'POST':
        post = get_object_or_404(News, id=request.POST.get('posts_id'))
        post.cat_id = get_object_or_404(Category, id=request.POST.get('cat_id'))
        post.subcategory_id = get_object_or_404(Subcategory, id=request.POST.get('subcat_id'))
        post.posttitle = request.POST.get('posttitle')
        post.postdetails = request.POST.get('postdetails')
        post.status = request.POST.get('status')
        if 'postimage' in request.FILES:
            post.postimage = request.FILES['postimage']
        post.save()
        messages.success(request, "Post updated Successfully!")
    return redirect('manage_posts')


# =====================================
# ========== WEBSITE PAGE MANAGEMENT =====
# =====================================

@login_required(login_url='/')
def WEBSITE_UPDATE(request):
    if request.method == "POST":
        page = get_object_or_404(Page, id=request.POST.get('web_id'))
        page.pagetitle = request.POST.get('pagetitle')
        page.address = request.POST.get('address')
        page.aboutus = request.POST.get('aboutus')
        page.mobilenumber = request.POST.get('mobilenumber')
        page.email = request.POST.get('email')
        page.save()
        messages.success(request, "Website updated Successfully!")
        return redirect('website_update')

    pages = Page.objects.all()
    return render(request, 'admin/website.html', {"pages": pages})


# =====================================
# ========== COMMENTS MANAGEMENT =========
# =====================================

@login_required(login_url='/')
def ALL_COMMENTS(request):
    all_comm = Comments.objects.all()
    paginator = Paginator(all_comm, 10)
    page_number = request.GET.get('page')
    try:
        all_comm = paginator.page(page_number)
    except PageNotAnInteger:
        all_comm = paginator.page(1)
    except EmptyPage:
        all_comm = paginator.page(paginator.num_pages)
    return render(request,'admin/all_comments.html',{'all_comm': all_comm})


@login_required(login_url='/')
def APPROVED_COMMENTS(request):
    approved_comm = Comments.objects.filter(status='Approved')
    paginator = Paginator(approved_comm, 10)
    page_number = request.GET.get('page')
    try:
        approved_comm = paginator.page(page_number)
    except PageNotAnInteger:
        approved_comm = paginator.page(1)
    except EmptyPage:
        approved_comm = paginator.page(paginator.num_pages)
    return render(request,'admin/comments_approved.html',{'approved_comm': approved_comm})


@login_required(login_url='/')
def UNAPPROVED_COMMENTS(request):
    unapproved_comm = Comments.objects.filter(status='Unapproved')
    paginator = Paginator(unapproved_comm, 10)
    page_number = request.GET.get('page')
    try:
        unapproved_comm = paginator.page(page_number)
    except PageNotAnInteger:
        unapproved_comm = paginator.page(1)
    except EmptyPage:
        unapproved_comm = paginator.page(paginator.num_pages)
    return render(request,'admin/comments_unapproved.html',{'unapproved_comm': unapproved_comm})


@login_required(login_url='/')
def VIEW_COMMENTS(request, id):
    comment = get_object_or_404(Comments, id=id)
    return render(request,'admin/view-comments-details.html',{'view_comments': comment})


@login_required(login_url='/')
def UPDATE_COMMENTS_STATUS(request):
    if request.method == 'POST':
        comment = get_object_or_404(Comments, id=request.POST.get('comm_id'))
        comment.status = request.POST.get('status')
        comment.save()
        messages.success(request, "Comment status updated Successfully!")
    return redirect('all_comments')


@login_required(login_url='/')
def DELETE_COMMENTS(request, id):
    get_object_or_404(Comments, id=id).delete()
    messages.success(request,'Record Deleted Successfully!')
    return redirect('all_comments')
