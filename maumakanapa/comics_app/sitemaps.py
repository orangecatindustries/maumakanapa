from django.contrib.sitemaps import Sitemap
from .models import webcomic
from django.urls import reverse

class comicSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return webcomic.objects.all()

    def location(self, obj):
        return reverse('comic_list', kwargs={'lang': obj.language})

class staticSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return webcomic.objects.all()

    def location(self, obj):
        return reverse('page', kwargs={'lang': obj.language, 'number': obj.ep_number})