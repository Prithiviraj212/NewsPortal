from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# ========================
# Custom User Model
# ========================
class CustomUser(AbstractUser):
    USER_TYPES = (
        (1, 'admin'),
        (2, 'subadmin'),
    )
    user_type = models.CharField(choices=USER_TYPES, max_length=50, default=1)
    profile_pic = models.ImageField(upload_to='media/profile_pic', blank=True, null=True)

    def __str__(self):
        return self.username

# ========================
# Category Model
# ========================
class Category(models.Model):
    catname = models.CharField(max_length=200)
    catdes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.catname

# ========================
# Subcategory Model
# ========================
class Subcategory(models.Model):
    cat_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcatname = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subcatname

# ========================
# News Model
# ========================
class News(models.Model):
    cat_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory_id = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    posttitle = models.CharField(max_length=250, blank=True)
    postdetails = models.TextField(blank=True)
    status = models.CharField(max_length=50, default='draft')  # draft/published
    postimage = models.ImageField(upload_to='media/news', blank=True, null=True)
    postedby = models.CharField(max_length=50, blank=True)
    posted_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updatedby = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.posttitle if self.posttitle else "Untitled News"

# ========================
# Page Model (About Us / Contact)
# ========================
class Page(models.Model):
    pagetitle = models.CharField(max_length=250)
    address = models.CharField(max_length=250, blank=True)
    aboutus = models.TextField(blank=True)
    email = models.EmailField(max_length=200, blank=True)
    mobilenumber = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pagetitle

# ========================
# Comments Model
# ========================
class Comments(models.Model):
    news_id = models.ForeignKey(News, on_delete=models.CASCADE)
    comment = models.TextField()
    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    status = models.CharField(max_length=250, blank=True)
    posted_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.news_id.posttitle}"

# ========================
# Contact Model
# ========================
class Contact(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    message = models.TextField()
    posted_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"
