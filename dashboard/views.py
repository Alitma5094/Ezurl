import random

import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django_htmx.http import HttpResponseClientRefresh
from qr_code.qrcode.utils import QRCodeOptions

from shorts.models import Short
from .forms import ShortForm

stripe.api_key = settings.STRIPE_SECRET_KEY


def generate_random_string(length=10):
    # Custom list to avoid ambiguous characters
    characters_list = [
        "c",
        "d",
        "e",
        "f",
        "h",
        "j",
        "k",
        "m",
        "n",
        "p",
        "r",
        "t",
        "v",
        "w",
        "x",
        "y",
        "2",
        "3",
        "4",
        "5",
        "6",
        "8",
        "9",
    ]
    return "".join(random.choice(characters_list) for _ in range(length))


@login_required()
def home_view(request):
    shortened_urls = Short.objects.filter(user=request.user)
    return render(
        request, "dashboard/home.html", context={"shortened_urls": shortened_urls}
    )


@login_required()
def shorts_form_view(request):
    if request.method == "POST":
        form = ShortForm(request.POST)

        if not form.is_valid():
            return render(request, "dashboard/shorts_form.html", context={"form": form})

        if not request.user.can_create_custom_url() and form.cleaned_data["back_half"]:
            form.add_error(
                "back_half",
                "You have reached the maximum number of custom short URLs.",
            )
            return render(request, "dashboard/shorts_form.html", context={"form": form})

        short = form.save(commit=False)
        short.user = request.user
        if not short.back_half:
            short.back_half = generate_random_string()
        short.save()
        return HttpResponseClientRefresh()

    return render(request, "dashboard/shorts_form.html", {"form": ShortForm()})


@login_required()
def short_detail_modal(request, pk):
    short = get_object_or_404(Short, id=pk)
    if request.method == "POST":
        short.background_color = request.POST.get("background-color")
        short.foreground_color = request.POST.get("foreground-color")
        short.save(update_fields=["foreground_color", "background_color"])

    background_color = short.background_color
    foreground_color = short.foreground_color

    qr_options = QRCodeOptions(
        image_format="png",
        size="m",
        light_color=background_color,
        dark_color=foreground_color,
    )
    default_values = {"background": background_color, "foreground": foreground_color}

    return render(
        request,
        "dashboard/short_detail_modal.html",
        context={
            "short": short,
            "qr_options": qr_options,
            "default_values": default_values,
            "qr_url": f"https://ezurl.dev/r/{short.back_half}",
        },
    )


@login_required()
@require_POST
def delete_url_view(request, pk):
    short = get_object_or_404(Short, id=pk)
    short.delete()
    return HttpResponseClientRefresh()
