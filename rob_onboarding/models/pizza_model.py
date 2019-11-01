from microcosm_postgres.models import EntityMixin, Model
from sqlalchemy import Column, Integer, String
from sqlalchemy_utils import UUIDType


class Pizza(EntityMixin, Model):

    __tablename__ = "pizza"

    customer_id = Column(UUIDType, nullable=False)
    size = Column(Integer, nullable=False, default=10)
    # TODO: Update field to use ChoiceType sqlalchemy to restrict choices
    crust_type = Column(String, nullable=False, unique=False, default="thin")
