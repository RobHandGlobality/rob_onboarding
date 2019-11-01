"""
Order controller.

"""
from microcosm.api import binding
from microcosm_flask.conventions.crud_adapter import CRUDStoreAdapter
from microcosm_flask.namespaces import Namespace

from rob_onboarding.models.order_event_type import OrderEventType
from rob_onboarding.models.order_model import Order


@binding("order_controller")
class OrderController(CRUDStoreAdapter):
    def __init__(self, graph):
        super().__init__(graph, graph.order_store)
        self.order_event_factory = graph.order_event_factory
        self.ns = Namespace(subject=Order, version="v1")

    def create(self, **kwargs):
        order = super().create(**kwargs)

        self.order_event_factory.create(
            ns=self.ns,
            sns_producer=None,
            order_id=order.id,
            event_type=OrderEventType.OrderInitialized,
        )
        return order

    def update(self, **kwargs):
        order = super().update(**kwargs)
        return order
