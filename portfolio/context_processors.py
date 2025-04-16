from .models import SiteSettings

def site_settings(request):
    """
    Context processor that provides site settings to all templates
    """
    settings = SiteSettings.objects.first()
    if not settings:
        settings = SiteSettings.objects.create()
    
    return {
        'site_settings': settings
    }