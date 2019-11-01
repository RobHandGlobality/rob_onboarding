"""
Topping CRUD routes.

"""
from microcosm.api import binding
from microcosm_flask.conventions.base import EndpointDefinition
from microcosm_flask.conventions.crud import configure_crud
from microcosm_flask.operations import Operation
from microcosm_postgres.context import transactional

from rob_onboarding.resources.topping_resources import (
    NewToppingSchema,
    SearchToppingSchema,
    ToppingSchema,
)


@binding("topping_routes")
def configure_topping_routes(graph):
    controller = graph.topping_controller
    mappings = {
        Operation.Create: EndpointDefinition(
            func=transactional(controller.create),
            request_schema=NewToppingSchema(),
            response_schema=ToppingSchema(),
        ),
        Operation.Delete: EndpointDefinition(
            func=transactional(controller.delete),
        ),
        Operation.Replace: EndpointDefinition(
            func=transactional(controller.replace),
            request_schema=NewToppingSchema(),
            response_schema=ToppingSchema(),
        ),
        Operation.Retrieve: EndpointDefinition(
            func=controller.retrieve,
            response_schema=ToppingSchema(),
        ),
        Operation.Search: EndpointDefinition(
            func=controller.search,
            request_schema=SearchToppingSchema(),
            response_schema=ToppingSchema(),
        ),
    }
    configure_crud(graph, controller.ns, mappings)
    return controller.ns
