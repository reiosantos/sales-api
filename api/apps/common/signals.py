from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save)
def generate_model_ref(sender, instance=None, created=False, **kwargs):
	list_of_models = (
		'User', 'ItemType', 'ItemSale', 'Customer'
	)
	if sender.__name__ in list_of_models:
		if created:
			if hasattr(instance, 'generate_ref'):
				instance.generate_ref()
				instance.save()
