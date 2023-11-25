from django import forms
from shorts.models import Short


class ShortForm(forms.ModelForm):
    redirect_url = forms.URLField(required=True)
    back_half = forms.SlugField(required=True, max_length=50,
                                error_messages={"invalid": "Please use only letters, numbers, underscores, or hyphens"})

    # back_half = forms.CharField(required=True, max_length=50)

    class Meta:
        model = Short
        exclude = ("user", "background_color", "foreground_color")
