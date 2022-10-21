from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import OrderLineItems


@receiver(post_save, sender=OrderLineItems)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update order total when line items
    are updated or created
    """
    instance.order.update_total()


@receiver(post_delete, sender=OrderLineItems)
def update_on_delete(sender, instance, **kwargs):
    """
    Update order total when a line
    item is deleted
    """
    instance.order.update_total()