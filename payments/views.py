import json
import stripe
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

@login_required()
def payments_subscribe(request):
    return render(request, "payments/subscribe.html", context={"subscribed": request.user.subscription_active})


@login_required()
def create_portal(request):
    portal_session = stripe.billing_portal.Session.create(
        customer=request.user.stripe_customer_id,
        return_url=request.META['HTTP_REFERER'],
    )
    return redirect(portal_session.url)


@login_required()
def create_checkout(request):
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
