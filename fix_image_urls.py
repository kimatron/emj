# Create a file called fix_image_urls.py in your project root
# Then run it with: python manage.py shell < fix_image_urls.py

from portfolio.models import Album, Photo

print('Starting URL path correction...')

# Fix Album cover images
albums = Album.objects.all()
print(f'Processing {albums.count()} albums...')

for album in albums:
    if album.cover_image and '/emjcamera/' not in album.cover_image.name and not album.cover_image.name.startswith('emjcamera/'):
        old_path = album.cover_image.name
        album.cover_image.name = f'emjcamera/{album.cover_image.name}'
        album.save(update_fields=['cover_image'])
        print(f'  Fixed album cover: {old_path} → {album.cover_image.name}')

# Fix Photo images
photos = Photo.objects.all()
print(f'Processing {photos.count()} photos...')

for photo in photos:
    if photo.image and '/emjcamera/' not in photo.image.name and not photo.image.name.startswith('emjcamera/'):
        old_path = photo.image.name
        photo.image.name = f'emjcamera/{photo.image.name}'
        photo.save(update_fields=['image'])
        print(f'  Fixed photo: {old_path} → {photo.image.name}')
    
    if photo.thumbnail and '/emjcamera/' not in photo.thumbnail.name and not photo.thumbnail.name.startswith('emjcamera/'):
        old_path = photo.thumbnail.name
        photo.thumbnail.name = f'emjcamera/{photo.thumbnail.name}'
        photo.save(update_fields=['thumbnail'])
        print(f'  Fixed thumbnail: {old_path} → {photo.thumbnail.name}')

print('URL correction completed!')