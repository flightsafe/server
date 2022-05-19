import enum


class MaintenanceProgress(enum.Enum):
    pending = "PENDING"
    in_progress = "IN_PROGRESS"
    finished = "FINISHED"


class MaintenanceStatus(enum.Enum):
    good_condition = "GOOD_CONDITION"
    bad_condition = "BAD_CONDITION"
    expired = "EXPIRED"
