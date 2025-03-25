from django.contrib import admin
from .models import Category, Album, Photo, Contact, SiteSettings

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date_created', 'is_featured', 'is_published')
    list_filter = ('category', 'is_featured', 'is_published')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [PhotoInline]

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'album', 'date_uploaded', 'is_featured')
    list_filter = ('album', 'is_featured')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'date_submitted', 'is_responded')
    list_filter = ('is_responded',)
    readonly_fields = ('name', 'email', 'phone', 'subject', 'message', 'date_submitted')

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Information', {
            'fields': ('site_title', 'tagline', 'about_text', 'about_image')
        }),
        ('Contact Information', {
            'fields': ('contact_info',)
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'instagram_url', 'twitter_url', 'pinterest_url')
        }),
    )

    def has_add_permission(self, request):
        # Only allow one instance of SiteSettings
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)