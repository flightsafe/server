import enum


class MaintenanceProgress(enum.Enum):
    pending = "PENDING"
    in_progress = "IN_PROGRESS"
    finished = "FINISHED"


class MaintenanceStatus(enum.Enum):
    good_condition = "GOOD_CONDITION"
    bad_condition = "BAD_CONDITION"
    expired = "EXPIRED"


class BookingStatus(enum.Enum):
    in_use = "IN_USE"
    not_in_use = "NOT_IN_USE"


class ErrorCode(enum.Enum):
    invalid = "invalid"
