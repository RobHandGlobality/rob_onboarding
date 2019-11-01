from microcosm_postgres.models import Model, UnixTimestampEntityMixin
from sqlalchemy import Column, String
from sqlalchemy_utils import UUIDType


class Topping(UnixTimestampEntityMixin, Model):
    __tablename__ = "topping"
    pizza_id = Column(UUIDType)
    topping_type = Column(String)
