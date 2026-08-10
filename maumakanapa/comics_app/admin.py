import re
from django import forms
from django.contrib import admin
from .models import webcomic, comicPage

def natural_sort_key(filename):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', filename)]

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        if isinstance(data, (list, tuple)):
            return [super(MultipleFileField, self).clean(d, initial) for d in data]
        return super().clean(data, initial)

class comicPageInline(admin.TabularInline):
    model = comicPage
    extra = 0
    fields = ('page_num', 'image')
    ordering = ('page_num',)

class WebcomicAdminForm(forms.ModelForm):
    bulk_images = MultipleFileField(
        required=False,
        help_text="add yo shit here twin"
    )

    class Meta:
        model = webcomic
        fields = '__all__'

@admin.register(webcomic)
class webcomicAdmin(admin.ModelAdmin):
    form = WebcomicAdminForm
    list_display = ('language', 'ep_number', 'title')
    list_filter = ('language',)
    search_fields = ('title', 'subtitle')
    inlines = [comicPageInline]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        files = form.cleaned_data.get('bulk_images')
        if files:
            files_sorted = sorted(files, key=lambda f: natural_sort_key(f.name))
            start_num = obj.pages.count() + 1
            for i, f in enumerate(files_sorted, start=start_num):
                comicPage.objects.create(webcomic=obj, image=f, page_num=i)