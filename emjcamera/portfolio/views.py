from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Category, Album, Photo, SiteSettings
from .forms import ContactForm

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