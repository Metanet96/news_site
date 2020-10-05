from django.http import Http404
from django.shortcuts import render ,redirect
from front import models, forms
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
from django.db.models import Q


def index(request):
    first_posts = models.Post.objects.filter(is_published =True).order_by('-id')[:6]
    other_posts = models.Post.objects.filter(is_published =True).order_by('-id')[6:9]
    nexts = models.Post.objects.filter(is_published =True).order_by('-id')[9:11]


    return render(request,'front/pages/index.html',{
        'first_posts': first_posts,
        'other_posts' : other_posts,
        'nexts' : nexts,

    })

# **********************************************************************************

def posts(request):
    categories = models.Category.objects.all()
    post_list = models.Post.objects.filter(is_published =True).order_by('-id')[:3]
    recents_posts = models.Post.objects.order_by('-id')[4:8]
    sport_posts1 =models.Post.objects.filter(is_published =True).filter(category__name = 'Sport').order_by('-id')[:1]
    sport_posts2 =models.Post.objects.filter(is_published =True).filter(category__name = 'Sport').order_by('-id')[1:2]
    sport_posts3 =models.Post.objects.filter(is_published =True).filter(category__name = 'Sport').order_by('-id')[2:3]
    sport_posts4 =models.Post.objects.filter(is_published =True).filter(category__name = 'Sport').order_by('-id')[3:4]
    style_posts =models.Post.objects.filter(is_published =True).filter(category__name = 'Style').order_by('-id')[:4]
    more_posts =models.Post.objects.filter(is_published =True).order_by('-id')[8:11]
    nexts = models.Post.objects.filter(is_published =True).order_by('-id')[11:13]

    return render(request,'front/pages/posts.html',{
        'categories' : categories,
        'post_list' : post_list,
        'recents_posts' : recents_posts,
        'sport_posts1' :sport_posts1,
        'sport_posts2' :sport_posts2,
        'sport_posts3' :sport_posts3,
        'sport_posts4' :sport_posts4,
        'style_posts' : style_posts,
        'more_posts' : more_posts,
        'nexts' : nexts,
    })

# **********************************************************************************

def post_details(request,slug):
    if not models.Post.objects.filter(is_published =True).filter(slug= slug).exists():
        raise Http404

    post = models.Post.objects.filter(is_published =True).get(slug=slug)
    previous_posts = models.Post.objects.filter(is_published =True).order_by('-id').filter(pk__lt = post.pk)[:1]
    next_posts = models.Post.objects.filter(is_published =True).order_by('-id').filter(pk__gt = post.pk)[:1]
    nexts = models.Post.objects.filter(is_published =True).order_by('-id')[:2]

    return render(request,'front/pages/post_details.html',{
        'slug' : slug,
        'post' : post,
        'next_posts' : next_posts,
        'previous_posts' : previous_posts,
        'nexts' : nexts,
    })

# **********************************************************************************

def post_author_details(request,redactor):
    if not models.Post.objects.filter(is_published =True).filter(author = redactor).exists():
        raise Http404

    first_post = models.Post.objects.filter(is_published =True).filter(author = redactor).order_by('-id')[:1]
    related_post = models.Post.objects.filter(is_published =True).filter(author = redactor).order_by('-id')[1:]
    nexts = models.Post.objects.filter(is_published =True).order_by('-id')[:2]

    return render(request,'front/pages/post_author_details.html',{
        'redactor' : redactor,
        'first_post' : first_post,
        'related_post' : related_post,
        'nexts' : nexts,
    })

# **********************************************************************************

def post_category_details(request,slug):
    if not models.Post.objects.filter(is_published =True).filter(category__slug = slug).exists():
        raise Http404

    category_posts = models.Post.objects.filter(is_published =True).filter(category__slug = slug).order_by('-id')
    nexts = models.Post.objects.filter(is_published =True).order_by('-id')[:2]

    paginator = Paginator(category_posts,4)
    page_number = request.GET.get('page')
    category_posts = paginator.get_page(page_number)

    return render(request,'front/pages/post_category_details.html',{
        'slug' : slug,
        'category_posts' : category_posts,
        'nexts' : nexts,
        'paginator' : paginator,
    })

# **********************************************************************************

def search_results(request):
       if ('q' in request.GET) :
        query_string = request.GET.get('q')
        posts = models.Post.objects.filter(Q(title__icontains=query_string)| Q(author__icontains=query_string) | Q(category__name__icontains=query_string))
        counts = posts.count()

        if posts:
            return render(request, 'front/pages/search_results.html', {
                'query_string': query_string,
                'posts': posts,
                'counts' : counts,
            })
        else:
            messages.warning(request, "Nothing found")
            return render(request,'front/pages/search_results.html',{
                'query_string': query_string,
                'posts': posts,
                'counts': counts,
            })

# **********************************************************************************

def add_posts(request):
    if request.user.is_anonymous :
        return redirect('front:auth_log_in')

    categories = models.Category.objects.all()
    form = forms.PostForm
    if request.POST:
        form = forms.PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Post successfully added but you need admin's permission")
            return redirect('front:posts')
        else:
            return redirect(request, 'front/add_posts.html')


    return render(request, 'front/pages/add_posts.html',{
        'categories' : categories,
        'form' : form,
    })

# **********************************************************************************

def auth_log_in(request):
    if request.user.is_authenticated:
        referrer = request.META.get('HTTP_REFERER')
        if not referrer:
            referrer = 'front:index'
        messages.warning(request, 'You already authenticated in system')
        return redirect(referrer)

    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user :
            login(request, user)
            return redirect('front:index')
        else:
            messages.warning(request, 'Credentials not valid')
            return redirect('front:auth_log_in')

    return render(request,'front/pages/auth/log_in.html')

# **********************************************************************************

def auth_sign_out(request):
    if request.user.is_anonymous:
        return redirect('front:auth_log_in')

    logout(request)

    return redirect('front:auth_log_in')

# **********************************************************************************

def auth_sign_in(request):
    if request.user.is_authenticated:
        referrer = request.META.get('HTTP_REFERER')
        if not referrer:
            referrer = 'front:index'
        messages.warning(request, 'You already authenticated in system')
        return redirect(referrer)

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, 'You are successfully registered')
            return redirect('front:index')
        else:
            messages.warning(request, 'Something was wrong please try again')
    form = SignUpForm()
    return render(request, 'front/pages/auth/sign_in.html', {'form': form})

# **********************************************************************************