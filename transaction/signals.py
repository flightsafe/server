from typing import Dict

from django.apps import apps
from django.core import exceptions
from django.db.models import Model
from django.db.models.signals import pre_save
from django.dispatch import receiver

from transaction.models import TransactionInfo, TransactionDetail


@receiver(pre_save, sender=TransactionInfo)
def validate_transaction(sender, instance: TransactionInfo, **kwargs):
    configs = apps.get_app_configs()
    details: TransactionDetail = TransactionDetail.from_dict(instance.details) if type(
        instance.details) == dict else instance.details

    if details:
        found_app = False
        for config in configs:
            if "site-packages" not in config.path:

                if config.label == details.app_label:
                    found_app = True
                    models: Dict[str, Model] = config.models
                    model_names = [model.__name__ for model in models.values()]
                    if details.model_name not in model_names:
                        raise exceptions.ValidationError({
                            "model_name": exceptions.ValidationError(f"model {details.model_name} not found")
                        })

        if not found_app:
            raise exceptions.ValidationError({
                "app_label": exceptions.ValidationError(f"App_label {details.app_label} not found")
            })
