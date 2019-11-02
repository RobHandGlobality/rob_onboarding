"""
OrderEvent persistence.

"""
from microcosm.api import binding
from microcosm_eventsource.stores import EventStore

from rob_onboarding.models.order_event_model import OrderEvent


@binding("order_event_store")
class OrderEventStore(EventStore):
    def __init__(self, graph):
        super().__init__(graph, OrderEvent, auto_filter_fields=(
            OrderEvent.event_type,
            OrderEvent.order_id,
        ))
