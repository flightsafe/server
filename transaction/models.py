from django.contrib.auth.models import User, AnonymousUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.apps import apps

from common.constants import TransactionName
from common.fields import DataclassJSONField
from common.types import TransactionDetail


class TransactionInfo(models.Model):
    name = models.CharField(max_length=128, choices=TransactionName.choices)
    details = DataclassJSONField(null=True, blank=True, help_text=_("Transaction details"),
                                 dataclass_cls=TransactionDetail)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def get_related_object(self):
        """
        Get related model object describe in the details field.
        :return:
        """
        details: TransactionDetail = self.details
        if details:
            model = apps.get_model(app_label=details.app_label, model_name=details.model_name)
            return model.objects.get(pk=details.pk)
