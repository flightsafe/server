from django.db import models


class MaintenanceProgress(models.TextChoices):
    pending = "PENDING"
    in_progress = "IN_PROGRESS"
    finished = "FINISHED"


class MaintenanceStatus(models.TextChoices):
    good_condition = "GOOD_CONDITION"
    bad_condition = "BAD_CONDITION"
    expired = "EXPIRED"


class BookingStatus(models.TextChoices):
    in_use = "IN_USE"
    not_in_use = "NOT_IN_USE"


class ErrorCode(models.TextChoices):
    invalid = "invalid"


class TransactionName(models.TextChoices):
    create_booking = "CREATE_BOOKING"
    delete_booking = "DELETE_BOOKING"
    create_lesson_record = "CREATE_LESSON_RECORD"
    create_comment = "CREATE_COMMENT"
    add_maintenance_item = "ADD_MAINTENANCE_ITEM"
    change_maintenance_status = "CHANGE_MAINTENANCE_STATUS"
    start_maintenance = "START_MAINTENANCE"
    end_maintenance = "END_MAINTENANCE"
