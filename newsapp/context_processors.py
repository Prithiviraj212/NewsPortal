from .models import Category, Page

# ========================
# Category Processor
# ========================
def category_processor(request):
    """
    Fetch all categories for navbar dropdown
    """
    categories = Category.objects.all()
    return {'cat': categories}


# ========================
# About Us / Page Processor
# ========================
def aboutus(request):
    """
    Fetch the first Page object for About Us info
    """
    first_page = Page.objects.first()
    return {'first_page': first_page}
