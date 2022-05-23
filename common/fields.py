from django.db import models

from dataclasses_json import DataClassJsonMixin


class DataclassJSONField(models.JSONField):
    dataclass_cls: DataClassJsonMixin

    def __init__(self, verbose_name=None, name=None, encoder=None, decoder=None, dataclass_cls=None, **kwargs):
        """
        Dataclass JSON Field will take a python dataclss object and convert it to json
        or take a json value from db and return a python dataclass object
        :param verbose_name:
        :param name:
        :param encoder:
        :param decoder:
        :param dataclass_cls: Dataclass class
        :param kwargs:
        """
        super().__init__(verbose_name, name, encoder, decoder, **kwargs)
        self.dataclass_cls = dataclass_cls

    def from_db_value(self, value, expression, connection):
        db_value = super().from_db_value(value, expression, connection)
        return self.dataclass_cls.from_dict(db_value)

    def get_prep_value(self, value: DataClassJsonMixin):
        json_value = value.to_dict()
        return super().get_prep_value(json_value)
