from hamcrest import assert_that, is_
from microcosm_postgres.context import SessionContext, transaction
from microcosm_postgres.identifiers import new_object_id

from rob_onboarding.app import create_app
from rob_onboarding.models.order_model import Order


class TestOrder:
    def setup(self):
        self.graph = create_app(testing=True)
        self.order_store = self.graph.order_store

        self.customer_id = new_object_id()

        self.context = SessionContext(self.graph)
        self.context.recreate_all()
        self.context.open()

    def teardown(self):
        self.context.close()
        self.graph.postgres.dispose()

    def test_create(self):
        """
        Order can be persisted
        """
        new_order = Order(customer_id=self.customer_id)

        with transaction():
            self.order_store.create(new_order)

        retrieved_order = self.order_store.retrieve(new_order.id)
        assert_that(retrieved_order, is_(new_order))
