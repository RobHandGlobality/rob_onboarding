from microcosm_postgres.models import EntityMixin, Model
from sqlalchemy import Column, Integer, String


class Pizza(EntityMixin, Model):

    __tablename__ = "pizza"

    customer_id = Column(Integer, nullable=False, unique=False)
    size = Column(Integer, nullable=False)
    # TODO: Update field to use ChoiceType sqlalchemy to restrict choices
    crust_type = Column(String, nullable=False, unique=False)
