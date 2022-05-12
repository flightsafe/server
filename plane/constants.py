import enum


class MaintenanceStatus(enum.Enum):
    pending = "PENDING"
    in_progress = "IN_PROGRESS"
    finished = "FINISHED"
