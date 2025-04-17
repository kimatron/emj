# Save this as undo_path_changes.py

from portfolio.models import Album, Photo

print('Starting URL path restoration...')

# Fix Album cover images
albums = Album.objects.all()
print(f'Processing {albums.count()} albums...')

for album in albums:
    if album.cover_image and album.cover_image.name.startswith('emjcamera/'):
        old_path = album.cover_image.name
        # Remove 'emjcamera/' prefix
        album.cover_image.name = album.cover_image.name.replace('emjcamera/', '', 1)
        album.save(update_fields=['cover_image'])
        print(f'  Restored album cover: {old_path} → {album.cover_image.name}')

# Fix Photo images
photos = Photo.objects.all()
print(f'Processing {photos.count()} photos...')

for photo in photos:
    if photo.image and photo.image.name.startswith('emjcamera/'):
        old_path = photo.image.name
        # Remove 'emjcamera/' prefix
        photo.image.name = photo.image.name.replace('emjcamera/', '', 1)
        photo.save(update_fields=['image'])
        print(f'  Restored photo: {old_path} → {photo.image.name}')
    
    if photo.thumbnail and photo.thumbnail.name.startswith('emjcamera/'):
        old_path = photo.thumbnail.name
        # Remove 'emjcamera/' prefix
        photo.thumbnail.name = photo.thumbnail.name.replace('emjcamera/', '', 1)
        photo.save(update_fields=['thumbnail'])
        print(f'  Restored thumbnail: {old_path} → {photo.thumbnail.name}')

print('URL path restoration completed!')