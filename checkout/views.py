from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings
import stripe
from basket.contexts import basket_contents
from .forms import OrderForm


def checkout(request):
    """
    Checkout View
    """
    stripe_public_key = settings.SRTIPE_PUBLIC_KEY
    stripe_secret_key = settings.SRTIPE_SECRET_KEY

    basket = request.session.get('basket', {})
    if not basket:
        messages.error(request, 'There is nothing in your basket!')
        return redirect(reverse('index'))

    current_basket = basket_contents(request)
    total = current_basket['grand_total']
    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, 'You are missing your public key. \
            Please make sure it is set!')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)
