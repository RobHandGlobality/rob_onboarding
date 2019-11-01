"""
Topping persistence.

"""
from microcosm.api import binding
from microcosm_postgres.store import Store

from rob_onboarding.models.topping_model import Topping


@binding("topping_store")
class ToppingStore(Store):

    def __init__(self, graph):
        super().__init__(self, Topping)

    def _order_by(self, query, **kwargs):
        return query.order_by(
            Topping.pizza_id.asc(),
        )
