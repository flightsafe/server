from dataclasses import dataclass
from typing import Any, Optional

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class TransactionDetail:
    """
    Store the related data of model
    """
    app_label: Optional[str] = None
    model_name: Optional[str] = None
    pk: Optional[Any] = None
