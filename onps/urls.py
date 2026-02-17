from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views, adminviews

urlpatterns = [
    # ================== HOME ==================
    path('', views.INDEX, name='home'),
    path('aboutus/', views.ABOUTUS, name='aboutus'),
    path('contactus/', views.CONTACTUS, name='contactus'),

    # ================== CATEGORY ==================
    path('category/<int:id>/', views.category_detail, name='category_detail'),

    # ================== SINGLE NEWS ==================
    path('view-single-news/<int:id>/', views.VIEW_SINGLENEWS, name='view_single_news'),

    # ================== SEARCH ==================
    path('search-news/', views.SEARCH_NEWS, name='search_news'),

    # ================== THANK YOU ==================
    path('thank-you/', views.THANKYOU, name='thank_you'),

    # ================== LOGIN / LOGOUT ==================
    path('login/', views.LOGIN, name='login'),
    path('do-login/', views.doLogin, name='doLogin'),
    path('logout/', views.doLogout, name='logout'),

    # ================== DASHBOARD ==================
    path('dashboard/', views.DASHBOARD, name='dashboard'),
    path('admin-profile/', views.ADMIN_PROFILE, name='admin_profile'),
    path('admin-profile/update/', views.ADMIN_PROFILE_UPDATE, name='admin_profile_update'),
    path('change-password/', views.CHANGE_PASSWORD, name='change_password'),

    # ================== SUBADMIN MANAGEMENT ==================
    path('admin/add-subadmin/', adminviews.ADD_SUBADMIN, name='add_subadmin'),
    path('admin/manage-subadmin/', adminviews.MANAGE_SUBADMIN, name='manage_subadmin'),
    path('admin/delete-subadmin/<int:id>/', adminviews.DELETE_SUBADMIN, name='delete_subadmin'),
    path('admin/view-subadmin/<int:id>/', adminviews.VIEW_SUBADMIN, name='view_subadmin'),
    path('admin/update-subadmin/', adminviews.SUBADMIN_PROFILE_UPDATE, name='update_subadmin_profile'),

    # ================== CATEGORY MANAGEMENT ==================
    path('admin/add-category/', adminviews.ADD_CATEGORY, name='add_category'),
    path('admin/manage-category/', adminviews.MANAGE_CATEGORY, name='manage_category'),
    path('admin/delete-category/<int:id>/', adminviews.DELETE_CATEGORY, name='delete_category'),
    path('admin/update-category/<int:id>/', adminviews.UPDATE_CATEGORY, name='update_category'),

    # ================== SUBCATEGORY MANAGEMENT ==================
    path('admin/add-subcategory/', adminviews.ADD_SUBCATEGORY, name='add_subcategory'),
    path('admin/manage-subcategory/', adminviews.MANAGE_SUBCATEGORY, name='manage_subcategory'),
    path('admin/delete-subcategory/<int:id>/', adminviews.DELETE_SUBCATEGORY, name='delete_subcategory'),
    path('admin/update-subcategory/<int:id>/', adminviews.UPDATE_SUBCATEGORY, name='update_subcategory'),

    # ================== POSTS ==================
    path('admin/add-post/', adminviews.ADD_POST, name='add_post'),
    path('admin/manage-posts/', adminviews.MANAGE_POSTS, name='manage_posts'),
    path('admin/delete-post/<int:id>/', adminviews.DELETE_POSTS, name='delete_post'),
    path('admin/views-posts/<int:id>/', adminviews.VIEWS_POSTS, name='views_posts'),  # ✅ ADDED THIS

    path('admin/update-post/', adminviews.UPDATE_POST, name='update_post'),

    # ================== COMMENTS MANAGEMENT ==================
    path('admin/all-comments/', adminviews.ALL_COMMENTS, name='all_comments'),
    path('admin/approved-comments/', adminviews.APPROVED_COMMENTS, name='approved_comments'),
    path('admin/unapproved-comments/', adminviews.UNAPPROVED_COMMENTS, name='unapproved_comments'),
    path('admin/view-comment/<int:id>/', adminviews.VIEW_COMMENTS, name='view_comment'),
    path('admin/update-comment-status/', adminviews.UPDATE_COMMENTS_STATUS, name='update_comment_status'),
    path('admin/delete-comment/<int:id>/', adminviews.DELETE_COMMENTS, name='delete_comment'),

    # ================== WEBSITE SETTINGS ==================
    path('admin/website-update/', adminviews.WEBSITE_UPDATE, name='website_update'),

    # ================== DJANGO ADMIN PANEL ==================
    path('django-admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
