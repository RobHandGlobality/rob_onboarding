"""
Pizza persistence.

"""
from microcosm.api import binding
from microcosm_postgres.store import Store

from rob_onboarding.models.pizza_model import Pizza


@binding("pizza_store")
class PizzaStore(Store):

    def __init__(self, graph):
        super().__init__(self, Pizza)

    def _order_by(self, query, **kwargs):
        return query.order_by(
            Pizza.customer_id.asc(),
        )
