from django.db import models

class webcomic(models.Model):
    LANGUAGE_CHOICES = [
        ('english', 'English'),
        ('indonesian', 'Indonesian'),
        ('spanish', 'Spanish'),
        ('portuguese', 'Portuguese'),
        ('russian', 'Russian'),
        ('chinese', 'Chinese'),
        ('italiano', 'Italiano'),
        ('filipino', 'Filipino')
    ]

    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES)
    ep_number = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        ordering = ['language', 'ep_number']
        unique_together = ('language', 'ep_number')

    def __str__(self):
        return f'[{self.language.upper()}] Ep {self.ep_number}: {self.title}'


class comicPage(models.Model):
    webcomic = models.ForeignKey(webcomic, related_name='pages', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='comics/pages/')
    page_num = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['webcomic', 'page_num']
        unique_together = ('webcomic', 'page_num')

    def __str__(self):
        return f"{self.webcomic.title} - Page {self.page_num}"