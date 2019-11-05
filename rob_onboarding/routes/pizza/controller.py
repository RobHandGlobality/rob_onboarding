"""
Pizza controller.

"""
from microcosm.api import binding
from microcosm_flask.conventions.crud_adapter import CRUDStoreAdapter
from microcosm_flask.namespaces import Namespace

from rob_onboarding.models.order_event_type import OrderEventType
from rob_onboarding.models.pizza_model import Pizza


@binding("pizza_controller")
class PizzaController(CRUDStoreAdapter):
    def __init__(self, graph):
        super().__init__(graph, graph.pizza_store)

        self.ns = Namespace(subject=Pizza, version="v1",)
        self.order_event_factory = graph.order_event_factory
        self.sns_producer = graph.sns_producer

    def create(self, **kwargs):
        pizza = super().create(**kwargs)

        self.order_event_factory.create(
            ns=None,
            sns_producer=self.sns_producer,
            order_id=pizza.order_id,
            event_type=OrderEventType.OrderInitialized,
        )
        return pizza
