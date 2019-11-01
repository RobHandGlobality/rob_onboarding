"""
OrderEvent controller.

"""
from microcosm.api import binding
from microcosm_flask.conventions.crud_adapter import CRUDStoreAdapter
from microcosm_flask.namespaces import Namespace

from rob_onboarding.models.order_event_model import OrderEvent


@binding("order_event_controller")
class OrderEventController(CRUDStoreAdapter):
    def __init__(self, graph):
        super().__init__(graph, graph.topping_store)

        self.order_event_factory = graph.order_event_factory
        self.ns = Namespace(subject=OrderEvent, version="v1",)

    @property
    def event_factory(self):
        return self.order_event_factory

    def create(self, event_type, **kwargs):
        return self.event_factory.create(self.ns, None, event_type=event_type, **kwargs)
