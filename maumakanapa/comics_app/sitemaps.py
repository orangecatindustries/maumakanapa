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
    priority = 0.5

    def items(self):
        languages = ["english", "indonesian", "spanish", "portuguese", "russian", "chinese", "filipino", "italiano"]
        static_items = []
        for lang in languages:
            static_items.append({'lang': lang, 'viewname': 'index'})
            static_items.append({'lang': lang, 'viewname': 'comic_list'})
            static_items.append({'lang': lang, 'viewname': 'about'})
        return static_items

    def location(self, item):
        return reverse(item['viewname'], kwargs={'lang': item['lang']})