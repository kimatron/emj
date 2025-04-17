# Create a file named fix_urls.py in your Django project root

from django.core.management.base import BaseCommand
from portfolio.models import Album, Photo  # Adjust import based on your actual app name
import os

class Command(BaseCommand):
    help = 'Fix existing URLs in the database for DigitalOcean Spaces storage'

    def handle(self, *args, **options):
        self.stdout.write('Starting URL path correction...')
        
        # Fix Album cover images
        albums = Album.objects.all()
        self.stdout.write(f'Processing {albums.count()} albums...')
        
        for album in albums:
            # Check if cover_image needs fixing
            if album.cover_image and '/emjcamera/' not in album.cover_image.name and not album.cover_image.name.startswith('emjcamera/'):
                # Store old path for reporting
                old_path = album.cover_image.name
                
                # Update path to include 'emjcamera/' prefix
                album.cover_image.name = f'emjcamera/{album.cover_image.name}'
                album.save(update_fields=['cover_image'])
                
                self.stdout.write(f'  Fixed album cover: {old_path} → {album.cover_image.name}')
        
        # Fix Photo images
        photos = Photo.objects.all()
        self.stdout.write(f'Processing {photos.count()} photos...')
        
        for photo in photos:
            # Check if image needs fixing
            if photo.image and '/emjcamera/' not in photo.image.name and not photo.image.name.startswith('emjcamera/'):
                # Store old path for reporting
                old_path = photo.image.name
                
                # Update path to include 'emjcamera/' prefix
                photo.image.name = f'emjcamera/{photo.image.name}'
                photo.save(update_fields=['image'])
                
                self.stdout.write(f'  Fixed photo: {old_path} → {photo.image.name}')
            
            # Check if thumbnail needs fixing
            if photo.thumbnail and '/emjcamera/' not in photo.thumbnail.name and not photo.thumbnail.name.startswith('emjcamera/'):
                # Store old path for reporting
                old_path = photo.thumbnail.name
                
                # Update path to include 'emjcamera/' prefix
                photo.thumbnail.name = f'emjcamera/{photo.thumbnail.name}'
                photo.save(update_fields=['thumbnail'])
                
                self.stdout.write(f'  Fixed thumbnail: {old_path} → {photo.thumbnail.name}')
        
        self.stdout.write(self.style.SUCCESS('URL correction completed!'))

# Place this file in 'portfolio/management/commands/fix_urls.py'
# Then run: python manage.py fix_urls