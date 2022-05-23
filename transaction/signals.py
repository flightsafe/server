from typing import Dict

from django.apps import apps
from django.core import exceptions
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db.models import Model
from django.contrib.auth.models import AnonymousUser

from transaction.models import TransactionInfo, TransactionDetail


@receiver(pre_save, sender=TransactionInfo)
def validating_lesson_history(sender, instance: TransactionInfo, **kwargs):
    configs = apps.get_app_configs()
    found_app = False
    details: TransactionDetail = instance.details

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
