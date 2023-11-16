from allauth.account.models import EmailAddress
from django.shortcuts import render, redirect, get_object_or_404
from shorts.models import Short
from .forms import ShortForm
from django.contrib.auth.decorators import login_required
from django_htmx.http import HttpResponseClientRefresh
from django.views.decorators.http import require_POST, require_GET
from allauth.account.forms import AddEmailForm
from allauth.account import signals
from allauth.account.adapter import get_adapter
from django.contrib import messages

import segno


@login_required()
def home_view(request):
    shortened_urls = Short.objects.filter(user=request.user)
    # qrcode = segno.make('https://www.simplifialltech.com/')
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
@require_GET
def short_detail_modal(request, pk):
    short = get_object_or_404(Short, id=pk)
    qrcode = segno.make(f"ezurl.dev/r/{short.back_half}/")
    return render(request, "dashboard/short_detail_modal.html",
                  context={"short": short, "qrcode": qrcode.svg_data_uri(scale=6)})


@login_required()
@require_POST
def delete_url_view(request, pk):
    short = get_object_or_404(Short, id=pk)
    short.delete()
    return HttpResponseClientRefresh()
