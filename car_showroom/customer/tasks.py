from celery import shared_task
from django.shortcuts import get_object_or_404
from .models import CustomerOffer
from .utils import get_cheapest_showroom_car, process_offered_car


@shared_task
def buy_offered_car(offer_id):
    offer = get_object_or_404(CustomerOffer, id=offer_id)
    customer = offer.customer
    model = offer.model

    showroom_car = get_cheapest_showroom_car(model)

    if showroom_car:
        process_offered_car(offer, showroom_car, customer, model)
