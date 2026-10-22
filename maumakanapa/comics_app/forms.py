from django import forms
from django.conf import settings

from .models import EpisodeComment


MAX_COMMENT_IMAGE_SIZE = settings.COMMENT_IMAGE_MAX_BYTES
ALLOWED_COMMENT_IMAGE_FORMATS = {'JPEG', 'PNG', 'GIF', 'WEBP'}


class CommentImageValidationMixin:
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image or getattr(image, '_committed', False):
            return image

        if image.size > MAX_COMMENT_IMAGE_SIZE:
            raise forms.ValidationError('Images and GIFs must be 5 MB or smaller.')

        detected_format = getattr(getattr(image, 'image', None), 'format', None)
        if detected_format not in ALLOWED_COMMENT_IMAGE_FORMATS:
            raise forms.ValidationError('Use a JPEG, PNG, GIF, or WebP image. Videos are not allowed.')

        width, height = image.image.size
        if (
            width > settings.COMMENT_IMAGE_MAX_DIMENSION
            or height > settings.COMMENT_IMAGE_MAX_DIMENSION
            or width * height > settings.COMMENT_IMAGE_MAX_PIXELS
        ):
            raise forms.ValidationError('Image dimensions exceed the allowed limit.')
        if getattr(image.image, 'n_frames', 1) > settings.COMMENT_IMAGE_MAX_FRAMES:
            raise forms.ValidationError('Animated images may contain at most 100 frames.')

        image.seek(0)
        image.name = f'upload.{detected_format.lower()}'
        return image


class CommentCreateForm(CommentImageValidationMixin, forms.ModelForm):
    class Meta:
        model = EpisodeComment
        fields = ('display_name', 'body', 'image')
        widgets = {
            'display_name': forms.TextInput(attrs={'maxlength': 32, 'autocomplete': 'nickname'}),
            'body': forms.Textarea(attrs={'rows': 4, 'maxlength': 2000}),
        }

    def clean_display_name(self):
        display_name = self.cleaned_data.get('display_name', '').strip() or 'Anonymous'
        if '[staff]' in display_name.casefold():
            raise forms.ValidationError('Only verified staff accounts can use the [STAFF] label.')
        return display_name

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('body', '').strip() and not cleaned_data.get('image'):
            raise forms.ValidationError('Add a message or an image before posting.')
        return cleaned_data


class CommentEditForm(CommentImageValidationMixin, forms.ModelForm):
    remove_image = forms.BooleanField(required=False)

    class Meta:
        model = EpisodeComment
        fields = ('body', 'image')
        widgets = {
            'body': forms.Textarea(attrs={'rows': 4, 'maxlength': 2000}),
        }

    def clean(self):
        cleaned_data = super().clean()
        has_image = bool(cleaned_data.get('image')) or (
            bool(self.instance.image) and not cleaned_data.get('remove_image')
        )
        if not cleaned_data.get('body', '').strip() and not has_image:
            raise forms.ValidationError('A post must contain a message or an image.')
        return cleaned_data


class CommentReportForm(forms.Form):
    reason = forms.CharField(
        max_length=500,
        min_length=5,
        strip=True,
        widget=forms.Textarea(attrs={
            'rows': 3,
            'maxlength': 500,
            'placeholder': 'Tell moderators why this comment should be reviewed.',
        }),
        error_messages={
            'min_length': 'Please give moderators a little more detail (at least 5 characters).',
        },
    )
