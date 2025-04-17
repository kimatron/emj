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

def debug_db(request):
    """A debug view to check database connections"""
    from django.http import HttpResponse
    from portfolio.models import Album, Category, SiteSettings, Photo
    
    html = ["<h1>Database Debug Info</h1>"]
    
    # Check SiteSettings
    html.append("<h2>Site Settings</h2>")
    site_settings = SiteSettings.objects.first()
    if site_settings:
        html.append(f"<p>Site Title: {site_settings.site_title}</p>")
        html.append(f"<p>Tagline: {site_settings.tagline}</p>")
        if site_settings.about_image:
            html.append(f"<p>About Image Path: {site_settings.about_image}</p>")
            html.append(f"<p>About Image URL: {site_settings.about_image.url}</p>")
            html.append(f"<img src='{site_settings.about_image.url}' style='max-width:300px'><hr>")
    else:
        html.append("<p>No site settings found</p>")
    
    # Check Albums
    html.append("<h2>Albums</h2>")
    albums = Album.objects.all()
    if albums:
        html.append(f"<p>Total Albums: {albums.count()}</p>")
        html.append(f"<p>Featured Albums: {Album.objects.filter(is_featured=True).count()}</p>")
        html.append(f"<p>Published Albums: {Album.objects.filter(is_published=True).count()}</p>")
        
        for album in albums:
            html.append(f"<h3>Album: {album.title}</h3>")
            html.append(f"<p>Published: {album.is_published} | Featured: {album.is_featured}</p>")
            html.append(f"<p>Category: {album.category.name}</p>")
            html.append(f"<p>Cover Image Path: {album.cover_image}</p>")
            html.append(f"<p>Cover Image URL: {album.cover_image.url}</p>")
            html.append(f"<img src='{album.cover_image.url}' style='max-width:300px'><hr>")
            
            # Check photos for this album
            photos = album.photos.all()
            html.append(f"<p>Number of photos: {photos.count()}</p>")
            if photos:
                first_photo = photos.first()
                html.append(f"<p>First Photo Path: {first_photo.image}</p>")
                html.append(f"<p>First Photo URL: {first_photo.image.url}</p>")
                html.append(f"<img src='{first_photo.image.url}' style='max-width:300px'><hr>")
    else:
        html.append("<p>No albums found</p>")
    
    # Check Categories
    html.append("<h2>Categories</h2>")
    categories = Category.objects.all()
    if categories:
        for category in categories:
            html.append(f"<p>Category: {category.name} - Albums: {category.albums.count()}</p>")
    else:
        html.append("<p>No categories found</p>")
    
    return HttpResponse("".join(html))

def debug_do(request):
    """Debug view for DigitalOcean connection"""
    from django.http import HttpResponse
    import boto3
    from django.conf import settings
    
    html = ["<h1>DigitalOcean Spaces Debug</h1>"]
    
    # Show settings
    html.append("<h2>Settings</h2>")
    html.append(f"<p>AWS_ACCESS_KEY_ID: {'✓ Set' if settings.AWS_ACCESS_KEY_ID else '✗ Not Set'}</p>")
    html.append(f"<p>AWS_SECRET_ACCESS_KEY: {'✓ Set' if settings.AWS_SECRET_ACCESS_KEY else '✗ Not Set'}</p>")
    html.append(f"<p>AWS_STORAGE_BUCKET_NAME: {settings.AWS_STORAGE_BUCKET_NAME}</p>")
    html.append(f"<p>AWS_S3_ENDPOINT_URL: {settings.AWS_S3_ENDPOINT_URL}</p>")
    html.append(f"<p>AWS_S3_CUSTOM_DOMAIN: {settings.AWS_S3_CUSTOM_DOMAIN}</p>")
    html.append(f"<p>AWS_DEFAULT_ACL: {settings.AWS_DEFAULT_ACL}</p>")
    
    # Try to connect to DigitalOcean
    try:
        s3 = boto3.client('s3',
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name='ams3'  # Adjust if needed
        )
        
        # List all objects in the bucket
        html.append("<h2>Files in Bucket</h2>")
        response = s3.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
        
        if 'Contents' in response:
            for obj in response['Contents']:
                key = obj['Key']
                # Make sure key is URL-encoded for direct access
                from urllib.parse import quote
                encoded_key = quote(key)
                url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{encoded_key}"
                
                html.append(f"<p>File: {key}</p>")
                html.append(f"<p>URL: <a href='{url}' target='_blank'>{url}</a></p>")
                if key.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    html.append(f"<img src='{url}' style='max-width:300px'><hr>")
                else:
                    html.append("<hr>")
        else:
            html.append("<p>No files found in bucket</p>")
            
    except Exception as e:
        html.append(f"<p>Error connecting to DigitalOcean: {str(e)}</p>")
    
    return HttpResponse("".join(html))

def debug_db_connection(request):
    """Debug view for database connection"""
    from django.http import HttpResponse
    from django.db import connections
    
    html = ["<h1>Database Connection Debug</h1>"]
    
    try:
        # Try to query something simple
        from django.contrib.auth.models import User
        user_count = User.objects.count()
        html.append(f"<p>Connection successful! User count: {user_count}</p>")
        
        # List all tables
        cursor = connections['default'].cursor()
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        tables = cursor.fetchall()
        html.append("<h2>Tables in database:</h2>")
        for table in tables:
            html.append(f"<p>{table[0]}</p>")
            
    except Exception as e:
        html.append(f"<p>Error connecting to database: {str(e)}</p>")
    
    return HttpResponse("".join(html))

def debug_settings(request):
    """Debug view for settings"""
    from django.http import HttpResponse
    from django.conf import settings
    
    html = ["<h1>Settings Debug</h1>"]
    
    # Show key settings
    html.append("<h2>Key Settings</h2>")
    html.append(f"<p>DEBUG: {settings.DEBUG}</p>")
    html.append(f"<p>ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}</p>")
    html.append(f"<p>STATIC_URL: {settings.STATIC_URL}</p>")
    html.append(f"<p>MEDIA_URL: {settings.MEDIA_URL}</p>")
    
    # DigitalOcean settings
    html.append("<h2>DigitalOcean Settings</h2>")
    html.append(f"<p>AWS_ACCESS_KEY_ID: {'✓ Set' if settings.AWS_ACCESS_KEY_ID else '✗ Not Set'}</p>")
    html.append(f"<p>AWS_STORAGE_BUCKET_NAME: {settings.AWS_STORAGE_BUCKET_NAME}</p>")
    html.append(f"<p>AWS_S3_ENDPOINT_URL: {settings.AWS_S3_ENDPOINT_URL}</p>")
    html.append(f"<p>AWS_S3_CUSTOM_DOMAIN: {settings.AWS_S3_CUSTOM_DOMAIN}</p>")
    
    return HttpResponse("".join(html))