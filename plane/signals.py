from django.db.models.signals import post_save
from django.dispatch import receiver

from common.constants import TransactionName
from common.types import TransactionDetail
from plane.apps import PlaneConfig
from plane.models import MaintenanceRecordItem, MaintenanceRecord
from transaction.models import TransactionInfo


@receiver(post_save, sender=MaintenanceRecord)
def update_maintenance(sender, instance: MaintenanceRecord, **kwargs):
    detail = TransactionDetail(app_label=PlaneConfig.name,
                               model_name=MaintenanceRecordItem.__name__,
                               pk=instance.pk)
    TransactionInfo.objects.create(title=TransactionName.add_maintenance_item, details=detail, user=instance.author)


@receiver(post_save, sender=MaintenanceRecordItem)
def update_maintenance_item(sender, instance: MaintenanceRecordItem, **kwargs):
    detail = TransactionDetail(app_label=PlaneConfig.name,
                               model_name=MaintenanceRecordItem.__name__,
                               pk=instance.pk)
    TransactionInfo.objects.create(title=TransactionName.add_maintenance_item, details=detail, user=instance.operator)
