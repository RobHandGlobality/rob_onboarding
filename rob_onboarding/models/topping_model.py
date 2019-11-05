from microcosm_postgres.models import Model, UnixTimestampEntityMixin
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy_utils import UUIDType


class Topping(UnixTimestampEntityMixin, Model):
    __tablename__ = "topping"

    pizza_id = Column(UUIDType, ForeignKey("pizza.id"), nullable=True)  # TODO: Should be false
    topping_type = Column(String)
    order_id = Column(UUIDType, ForeignKey("order.id"), nullable=True)  # TODO: Should be false
