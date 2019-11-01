from microcosm_postgres.models import Model, UnixTimestampEntityMixin
from sqlalchemy import Column
from sqlalchemy_utils import UUIDType


class Order(UnixTimestampEntityMixin, Model):
    __tablename__ = 'order'
    customer_id = Column(UUIDType)
