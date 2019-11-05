from microcosm_eventsource.models import EventMeta
from microcosm_postgres.models import UnixTimestampEntityMixin
from six import add_metaclass
from sqlalchemy import Column
from sqlalchemy_utils import UUIDType

from rob_onboarding.models.order_event_type import OrderEventType
from rob_onboarding.models.order_model import Order


@add_metaclass(EventMeta)
class OrderEvent(UnixTimestampEntityMixin):
    __tablename__ = "order_event"
    __eventtype__ = OrderEventType
    __container__ = Order

    order_id = Column(UUIDType, nullable=False)
    # TODO Restore when migration fixed
    # customer_id = Column(UUIDType, nullable=False)
