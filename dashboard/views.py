from django.shortcuts import render, get_object_or_404
from shorts.models import Short
from .forms import ShortForm
from django.contrib.auth.decorators import login_required
from django_htmx.http import HttpResponseClientRefresh
from django.views.decorators.http import require_POST
from qr_code.qrcode.utils import QRCodeOptions


@login_required()
def home_view(request):
    shortened_urls = Short.objects.filter(user=request.user)
    form = ShortForm()
    return render(request, "dashboard/home.html", context={"shortened_urls": shortened_urls, "form": form})


@login_required()
def shorts_form_view(request):
    if request.method == "POST":
        form = ShortForm(request.POST)
        if form.is_valid():
            short = form.save(commit=False)
            short.user = request.user
            short.save()
            return HttpResponseClientRefresh()
        else:
            return render(request, "dashboard/shorts_form.html", context={"form": form})
    return render(request, "dashboard/shorts_form.html", {"form": ShortForm()})


@login_required()
def short_detail_modal(request, pk):
    short = get_object_or_404(Short, id=pk)
    if request.method == "POST":
        background_color = request.POST.get("background-color")
        foreground_color = request.POST.get("foreground-color")
    else:
        background_color = "#ffffff"
        foreground_color = "#000000"

    qr_options = QRCodeOptions(image_format="png", size="m", light_color=background_color, dark_color=foreground_color)
    default_values = {"background": background_color, "foreground": foreground_color}

    return render(request, "dashboard/short_detail_modal.html",
                  context={"short": short, "qr_options": qr_options, "default_values": default_values,
                           "qr_url": f"https://ezurl.dev/r/{short.back_half}"})


@login_required()
@require_POST
def delete_url_view(request, pk):
    short = get_object_or_404(Short, id=pk)
    short.delete()
    return HttpResponseClientRefresh()
