from django.contrib import admin
from .models import Category, Album, Photo, Contact, SiteSettings

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1
    fields = ('image', 'title', 'order', 'is_featured')

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date_created', 'photo_count', 'is_featured', 'is_published')
    list_filter = ('category', 'is_featured', 'is_published')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'description')
    inlines = [PhotoInline]
    list_editable = ('is_featured', 'is_published')

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'album', 'date_uploaded', 'is_featured')
    list_filter = ('album', 'is_featured')
    search_fields = ('title', 'description')
    list_editable = ('is_featured',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'date_submitted', 'is_responded')
    list_filter = ('is_responded', 'date_submitted')
    readonly_fields = ('name', 'email', 'phone', 'subject', 'message', 'date_submitted')
    search_fields = ('name', 'email', 'subject', 'message')
    list_editable = ('is_responded',)

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Site Information', {
            'fields': ('site_title', 'tagline')
        }),
        ('About Page', {
            'fields': ('about_text', 'about_image')
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