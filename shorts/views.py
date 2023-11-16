from django.shortcuts import render, redirect
from .models import Short
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.

def redirect_url(request, back_half):
    try:
        requested_short = Short.objects.get(back_half=back_half)
        return redirect(requested_short.redirect_url)
    except ObjectDoesNotExist:
        return render(request, "shorts/404.html", status=404)
