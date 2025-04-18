from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from .models import BlogPost, BlogCategory, BlogTag, Comment
from .forms import CommentForm

def blog_list(request):
    """View for displaying all published blog posts"""
    posts = BlogPost.objects.filter(
        status='published',
        published_at__lte=timezone.now()
    ).order_by('-published_at')
    
    # Get categories for sidebar
    categories = BlogCategory.objects.all()
    
    # Get featured posts
    featured_posts = BlogPost.objects.filter(
        status='published', 
        is_featured=True
    )[:3]
    
    # Pagination
    paginator = Paginator(posts, 6)  # 6 posts per page
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    context = {
        'posts': posts,
        'categories': categories,
        'featured_posts': featured_posts,
        'page_title': 'Blog | Photography Thoughts & Adventures',
        'meta_description': 'Join me on a journey through photography tips, behind-the-scenes stories, and the occasional existential crisis about whether that shot is actually in focus.'
    }
    return render(request, 'blog/blog_list.html', context)

def blog_detail(request, slug):
    """View for displaying a specific blog post and its comments"""
    post = get_object_or_404(
        BlogPost, 
        slug=slug,
        status='published',
        published_at__lte=timezone.now()
    )
    
    # Get related posts
    related_posts = BlogPost.objects.filter(
        status='published',
        category=post.category
    ).exclude(id=post.id)[:3]
    
    # Get comments
    comments = post.comments.filter(is_approved=True)
    
    # Comment form handling
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return redirect('blog_post_detail', slug=post.slug)
    else:
        comment_form = CommentForm()
    
    context = {
        'post': post,
        'related_posts': related_posts,
        'comments': comments,
        'comment_form': comment_form,
        'page_title': f'{post.title} | Blog',
        'meta_description': post.excerpt if post.excerpt else f'Read about {post.title} - {post.category.name} photography insights from Emilija Jefremova.'
    }
    return render(request, 'blog/blog_detail.html', context)

def blog_category(request, slug):
    """View for displaying blog posts filtered by category"""
    category = get_object_or_404(BlogCategory, slug=slug)
    posts = BlogPost.objects.filter(
        category=category,
        status='published',
        published_at__lte=timezone.now()
    ).order_by('-published_at')
    
    # Get all categories for sidebar
    categories = BlogCategory.objects.all()
    
    # Pagination
    paginator = Paginator(posts, 6)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    context = {
        'category': category,
        'posts': posts,
        'categories': categories,
        'page_title': f'{category.name} | Blog',
        'meta_description': f'Explore my {category.name} photography blog posts - tips, stories, and behind-the-scenes insights with a touch of Lithuanian flair.'
    }
    return render(request, 'blog/blog_category.html', context)

def blog_tag(request, slug):
    """View for displaying blog posts filtered by tag"""
    tag = get_object_or_404(BlogTag, slug=slug)
    posts = tag.posts.filter(
        status='published',
        published_at__lte=timezone.now()
    ).order_by('-published_at')
    
    # Get categories for sidebar
    categories = BlogCategory.objects.all()
    
    # Pagination
    paginator = Paginator(posts, 6)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    context = {
        'tag': tag,
        'posts': posts,
        'categories': categories,
        'page_title': f'{tag.name} | Blog',
        'meta_description': f'Articles tagged with {tag.name} - photography insights and adventures from Emilija Jefremova.'
    }
    return render(request, 'blog/blog_tag.html', context)