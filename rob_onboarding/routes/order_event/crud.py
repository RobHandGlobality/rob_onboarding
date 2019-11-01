"""
OrderEvent CRUD routes.

"""
from microcosm.api import binding
from microcosm_flask.conventions.base import EndpointDefinition
from microcosm_flask.conventions.crud import configure_crud
from microcosm_flask.operations import Operation

from rob_onboarding.resources.order_event_resources import OrderEventSchema, SearchOrderEventSchema


@binding("order_event_routes")
def configure_order_routes(graph):
    controller = graph.order_event_controller
    mappings = {
        Operation.Retrieve: EndpointDefinition(
            func=controller.retrieve, response_schema=OrderEventSchema(),
        ),
        Operation.Search: EndpointDefinition(
            func=controller.search,
            request_schema=SearchOrderEventSchema(),
            response_schema=OrderEventSchema(),
        ),
    }
    configure_crud(graph, controller.ns, mappings)
    return controller.ns
