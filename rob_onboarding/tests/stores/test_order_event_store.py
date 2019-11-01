from hamcrest import assert_that, is_
from microcosm_postgres.context import SessionContext, transaction
from microcosm_postgres.identifiers import new_object_id

from rob_onboarding.app import create_app
from rob_onboarding.models.order_event_model import OrderEvent
from rob_onboarding.models.order_event_type import OrderEventType
from rob_onboarding.models.order_model import Order


class TestOrderEvent:
    def setup(self):
        self.graph = create_app(testing=True)
        self.order_event_store = self.graph.order_event_store

        self.order_id = new_object_id()

        self.context = SessionContext(self.graph)
        self.context.recreate_all()
        self.context.open()

    def teardown(self):
        self.context.close()
        self.graph.postgres.dispose()

    def test_create(self):
        """
        OrderEvent can be persisted
        """
        new_order = Order(id=self.order_id)
        new_order_event = OrderEvent(
            order_id=self.order_id, event_type=OrderEventType.OrderInitialized
        )

        with transaction():
            self.graph.order_store.create(new_order)
            self.order_event_store.create(new_order_event)

        retrieved_order_event = self.order_event_store.retrieve(new_order_event.id)
        assert_that(retrieved_order_event, is_(new_order_event))
