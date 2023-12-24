from django import forms
from shorts.models import Short


class ShortForm(forms.ModelForm):
    redirect_url = forms.URLField(required=True)
    back_half = forms.SlugField(required=False, max_length=50,
                                error_messages={"invalid": "Please use only letters, numbers, underscores, or hyphens"},
                                help_text="Leave blank to generate a random short URL", label="Back Half (Optional)")

    class Meta:
        model = Short
        exclude = ("user", "background_color", "foreground_color", "custom_back_half")
