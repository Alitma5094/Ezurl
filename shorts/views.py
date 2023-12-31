from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

from .models import Short


# Create your views here.


def redirect_url(request, back_half):
    try:
        requested_short = Short.objects.get(back_half=back_half)
        return render(
            request, "shorts/redirect.html", context={"redirect_url": requested_short}
        )
    except ObjectDoesNotExist:
        return render(request, "shorts/404.html", status=404)
