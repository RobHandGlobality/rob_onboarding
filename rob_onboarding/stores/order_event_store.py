"""
OrderEvent persistence.

"""
from microcosm.api import binding
from microcosm_postgres.store import Store

from rob_onboarding.models.order_event_model import OrderEvent


@binding("order_event_store")
class OrderEventStore(Store):
    def __init__(self, graph):
        super().__init__(graph, OrderEvent)

    def retrieve_most_recent(self, order_id, **kwargs):
        return OrderEvent.search(order_id=order_id)
