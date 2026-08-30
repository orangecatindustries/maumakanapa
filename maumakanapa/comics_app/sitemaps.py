from django.contrib.sitemaps import Sitemap
from .models import webcomic
from django.urls import reverse

class staticSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        languages = ["english", "indonesian", "spanish", "portuguese", "russian", "chinese", "filipino", "italiano"]
        static_items = []
        for lang in languages:
            static_items.append({'lang': lang, 'viewname': 'index'})
            static_items.append({'lang': lang, 'viewname': 'comic_list'})
            static_items.append({'lang': lang, 'viewname': 'about'})
            static_items.append({'lang': lang, 'viewname': 'revindex'})
            static_items.append({'lang': lang, 'viewname': 'tsrfindex'})
            static_items.append({'lang': lang, 'viewname': 'tbtlindex'})
            static_items.append({'lang': lang, 'viewname': 'tsrfindex'})
        return static_items

    def location(self, item):
        return reverse(item['viewname'], kwargs={'lang': item['lang']})

class comicSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return webcomic.objects.all()

    def location(self, obj):
        return reverse('page', kwargs={'lang': obj.language, 'number': obj.ep_number})