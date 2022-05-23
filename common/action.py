import enum


class ActionEnum(enum.Enum):
    list = "list"
    retrieve = "retrieve"
    create = "create"
    update = "partial_update"
    delete = "destroy"
