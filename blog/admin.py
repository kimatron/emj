from django.contrib import admin
from django.utils import timezone
from .models import BlogCategory, BlogTag, BlogPost, Comment

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.action(description='Mark selected posts as published')
def make_published(modeladmin, request, queryset):
    queryset.update(status='published', published_at=timezone.now())

@admin.action(description='Mark selected posts as draft')
def make_draft(modeladmin, request, queryset):
    queryset.update(status='draft')

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'created_at', 'is_featured')
    list_filter = ('status', 'category', 'tags', 'is_featured', 'created_at')
    search_fields = ('title', 'content', 'excerpt')
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ['category', 'tags']
    filter_horizontal = ('tags',)
    actions = [make_published, make_draft]
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'author', 'featured_image', 'excerpt', 'content')
        }),
        ('Categorization', {
            'fields': ('category', 'tags')
        }),
        ('Status & Settings', {
            'fields': ('status', 'is_featured', 'published_at')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        
        # Set published_at date when post is published
        if obj.status == 'published' and not obj.published_at:
            obj.published_at = timezone.now()
            
        super().save_model(request, obj, form, change)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'created_at', 'is_approved')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('name', 'email', 'content')
    actions = ['approve_comments']
    
    @admin.action(description='Approve selected comments')
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)