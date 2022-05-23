from dataclasses import dataclass
from typing import Any

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class TransactionDetail:
    """
    Store the related data of model
    """
    app_label: str
    model_name: str
    pk: Any
