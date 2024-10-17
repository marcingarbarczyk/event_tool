from PIL import Image
import io

from django.core.files.base import ContentFile

from apps.events.models import News


def create_image():
    try:
        # Create a blank 800x600 image with a white background
        img = Image.new('RGB', (800, 600), (128, 128, 128))
        img_io = io.BytesIO()
        img.save(img_io, format='JPEG')
        img_io.seek(0)

        return ContentFile(img_io.getvalue(), 'news_image.jpg')
    except Exception as e:
        return None

news_objects = News.objects.all()
for news in news_objects:
    news.image.save(f'news_{news.id}.jpg', create_image())
