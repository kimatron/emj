from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Category, Album, Photo, SiteSettings
from .forms import ContactForm

# Add this to your portfolio/views.py

def debug_media(request):
    """A debug view to check media URLs and connections"""
    from django.http import HttpResponse
    from django.conf import settings  # Add this import
    from portfolio.models import Album  # Adjust based on your model with images
    
    html = ["<h1>Media Debug Info</h1>"]
    
    # Environment settings
    html.append("<h2>Storage Settings</h2>")
    html.append(f"<p>MEDIA_URL: {settings.MEDIA_URL}</p>")
    html.append(f"<p>AWS_S3_CUSTOM_DOMAIN: {settings.AWS_S3_CUSTOM_DOMAIN}</p>")
    html.append(f"<p>DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}</p>")
    
    # Check images
    html.append("<h2>Image URLs</h2>")
    albums = Album.objects.all()
    for album in albums:
        if album.cover_image:
            html.append(f"<p>Album: {album.title}</p>")
            html.append(f"<p>Image field value: {album.cover_image}</p>")
            html.append(f"<p>Image URL: {album.cover_image.url}</p>")
            html.append(f"<img src='{album.cover_image.url}' style='max-width:300px'><hr>")
    
    return HttpResponse("".join(html))

def get_site_settings():
    """Helper function to get site settings"""
    return SiteSettings.objects.first() or SiteSettings.objects.create()

def home(request):
    """Homepage view"""
    featured_albums = Album.objects.filter(is_featured=True, is_published=True)[:6]
    site_settings = get_site_settings()
    
    context = {
        'featured_albums': featured_albums,
        'site_settings': site_settings,
    }
    return render(request, 'portfolio/index.html', context)

def about(request):
    """About page view"""
    site_settings = get_site_settings()
    
    context = {
        'site_settings': site_settings,
    }
    return render(request, 'portfolio/about.html', context)

def contact(request):
    """Contact page view with form handling"""
    site_settings = get_site_settings()
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent. Thank you!")
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
        'site_settings': site_settings,
    }
    return render(request, 'portfolio/contact.html', context)

def album_list(request):
    """View for displaying all published albums"""
    albums = Album.objects.filter(is_published=True)
    categories = Category.objects.all()
    site_settings = get_site_settings()
    
    context = {
        'albums': albums,
        'categories': categories,
        'site_settings': site_settings,
    }
    return render(request, 'portfolio/album_list.html', context)

def album_detail(request, slug):
    """View for displaying a specific album and its photos"""
    album = get_object_or_404(Album, slug=slug, is_published=True)
    photos = album.photos.all()
    
    # Get the next album for the "next album" section
    try:
        next_album = Album.objects.filter(
            is_published=True, 
            order__gt=album.order
        ).order_by('order').first()
        
        if not next_album:
            # If no album with higher order, get the first album (circular)
            next_album = Album.objects.filter(
                is_published=True
            ).exclude(id=album.id).order_by('order').first()
    except:
        next_album = None
    
    context = {
        'album': album,
        'photos': photos,
        'next_album': next_album,
    }
    return render(request, 'portfolio/album_detail.html', context)