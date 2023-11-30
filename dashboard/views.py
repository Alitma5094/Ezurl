from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt

from shorts.models import Short
from .forms import ShortForm
from django.contrib.auth.decorators import login_required
from django_htmx.http import HttpResponseClientRefresh
from django.views.decorators.http import require_POST
from qr_code.qrcode.utils import QRCodeOptions
import stripe
from django.conf import settings
import json
from django.http import HttpResponse

stripe.api_key = settings.STRIPE_SECRET_KEY


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
        short.background_color = request.POST.get("background-color")
        short.foreground_color = request.POST.get("foreground-color")
        short.save(update_fields=["foreground_color", "background_color"])

    background_color = short.background_color
    foreground_color = short.foreground_color

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


@login_required()
def payments_subscribe(request):
    if request.method == "POST":
        price_id = settings.STRIPE_PRICE_ID
        if request.user.stripe_customer_id:
            session = stripe.checkout.Session.create(
                success_url=request.META['HTTP_REFERER'] + "?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=request.META['HTTP_REFERER'], mode="subscription",
                line_items=[{"price": price_id, "quantity": 1}],
                client_reference_id=request.user.id,
                customer=request.user.stripe_customer_id
            )
        else:
            session = stripe.checkout.Session.create(
                success_url=request.META['HTTP_REFERER'] + "?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=request.META['HTTP_REFERER'], mode="subscription",
                line_items=[{"price": price_id, "quantity": 1}],
                client_reference_id=request.user.id,
                customer_email=request.user.email)
        return redirect(session.url)

    return render(request, "payments/subscribe.html", context={"subscribed": request.user.subscription_active})


@login_required()
def customer_portal(request):
    portal_session = stripe.billing_portal.Session.create(
        customer=request.user.stripe_customer_id,
        return_url=request.META['HTTP_REFERER'],
    )
    return redirect(portal_session.url)


@csrf_exempt
def stripe_webhooks(request):
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET
    request_data = json.loads(request.body)

    if webhook_secret:
        # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
        signature = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload=request.body, sig_header=signature, secret=webhook_secret)
            data = event['data']
        except Exception as e:
            return e
        # Get the type of webhook event sent - used to check the status of PaymentIntents.
        event_type = event['type']
    else:
        data = request_data['data']
        event_type = request_data['type']
    data_object = data['object']

    print(event_type)
    if event_type == 'checkout.session.completed':
        # Payment is successful and the subscription is created.
        # You should provision the subscription and save the customer ID to your database.
        user = get_user_model().objects.get(id=data_object['client_reference_id'])
        user.stripe_customer_id = data_object['customer']
        user.save()
        print(data)
    elif event_type == 'invoice.paid':
        user = get_user_model().objects.get(stripe_customer_id=data_object['customer'])
        user.subscription_active = True
        user.save()
        print(data)
    elif event_type == 'customer.subscription.deleted':
        print('Subscription canceled')
        user = get_user_model().objects.get(stripe_customer_id=data_object['customer'])
        user.subscription_active = False
        user.save()

    return HttpResponse(status=200)
