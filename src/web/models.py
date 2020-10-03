from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver


def upload_location(instance, filename, **kwargs):
    file_path = 'news_images/{title}-{file_name}'.format(
        title=str(instance.title), file_name=filename
    )
    return file_path


class News(models.Model):
    news_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, null=False, blank=False)
    body = models.TextField(max_length=5000, null=False, blank=False)
    image = models.ImageField(upload_to=upload_location, null=False, blank=False)
    date_published = models.DateField(auto_now_add=True, verbose_name='Date Published')
    date_updated = models.DateField(auto_now_add=True, verbose_name='Date Updated')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reference_link = models.CharField(max_length=5000)
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'


@receiver(post_delete, sender=News)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)


def pre_save_news_receiver(sender, instance, **kwargs):
    if not instance.slug:
        print(instance.news_id)
        instance.slug = slugify(instance.title)


pre_save.connect(pre_save_news_receiver, sender=News)
