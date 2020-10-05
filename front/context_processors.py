from front import models


def menu (request):
    category_list_menu = models.Category.objects.all().filter(is_published_menu = True).filter(is_published_right = True)
    return {
        'category_list_menu' : category_list_menu,
    }

def right(request):
    category_list_right = models.Category.objects.all().filter(is_published_right = True)
    return {
        'category_list_right' : category_list_right,
    }

def authors (request):
    author_lists = models.Post.objects.filter(is_published =True).values('author').distinct()
    return {
        'author_lists' : author_lists,
    }

def recents (request):
    recent_posts = models.Post.objects.filter(is_published =True).order_by('-id')[:2]
    return {
        'recent_posts' : recent_posts,
    }

def allsocials(request):
    all_social_accounts = models.SocialAccounts.objects.all()
    return {
        'all_social_accounts' : all_social_accounts,
    }

def socials(request):
    social_accounts = models.SocialAccounts.objects.all()[:5]
    return {
        'social_accounts' : social_accounts,
    }

def comment (request):
    comments = models.Comment.objects.all()
    return {
        'comments' : comments
    }