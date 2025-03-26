from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User

class Category(models.Model):
    """Category for organizing albums (e.g., Portraits, Weddings, etc.)"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Album(models.Model):
    """Photo album/gallery"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='albums')
    cover_image = models.ImageField(upload_to='albums/covers/')
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', '-date_created']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('album_detail', kwargs={'slug': self.slug})
    
    @property
    def photo_count(self):
        return self.photos.count()

class Photo(models.Model):
    """Individual photo in an album"""
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='photos')
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='albums/photos/')
    thumbnail = models.ImageField(upload_to='albums/thumbnails/', blank=True)
    date_taken = models.DateTimeField(blank=True, null=True)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', '-date_uploaded']
    
    def __str__(self):
        return self.title or f"Photo {self.id}"
      
class Contact(models.Model):
    """Contact form submissions"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date_submitted = models.DateTimeField(auto_now_add=True)
    is_responded = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-date_submitted']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
      
class SiteSettings(models.Model):
    """Global site settings"""
    site_title = models.CharField(max_length=100, default="EmjCamera Photography")
    tagline = models.CharField(max_length=200, blank=True)
    about_text = models.TextField(blank=True)
    about_image = models.ImageField(upload_to='site/', blank=True)
    contact_info = models.TextField(blank=True)
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    pinterest_url = models.URLField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    
    class Meta:
        verbose_name_plural = "Site Settings"
    
    def __str__(self):
        return self.site_title