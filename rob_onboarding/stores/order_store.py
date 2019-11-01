"""
Order persistence.

"""
from microcosm.api import binding
from microcosm_postgres.store import Store

from rob_onboarding.models.order_model import Order


@binding("order_store")
class OrderStore(Store):
    def __init__(self, graph):
        super().__init__(graph, Order)
