from unittest.mock import patch

from hamcrest import (
    assert_that,
    contains,
    equal_to,
    has_entries,
    is_,
)
from microcosm_postgres.context import SessionContext, transaction
from microcosm_postgres.identifiers import new_object_id
from microcosm_postgres.operations import recreate_all

from rob_onboarding.app import create_app
from rob_onboarding.models.order_event_type import OrderEventType
from rob_onboarding.models.order_model import Order
from rob_onboarding.models.pizza_model import Pizza
from rob_onboarding.models.topping_model import Topping


class TestToppingRoutes:
    list_create_uri = "/api/v1/topping"

    def setup(self):
        self.graph = create_app(testing=True)
        self.client = self.graph.flask.test_client()
        recreate_all(self.graph)

        self.factory = self.graph.order_event_factory

        self.pizza_id = new_object_id()
        self.order_id = new_object_id()
        self.customer_id = new_object_id()
        self.topping_id = new_object_id()
        self.pizza = Pizza(id=self.pizza_id, customer_id=self.customer_id)
        self.order = Order(id=self.order_id, customer_id=self.customer_id)
        self.topping1 = Topping(
            id=self.topping_id,
            pizza_id=self.pizza_id,
            topping_type="ONION",
            order_id=self.order_id,
        )
        self.detail_uri = f"/api/v1/topping/{self.topping1.id}"

    def teardown(self):
        self.graph.postgres.dispose()

    def test_search(self):
        with SessionContext(self.graph), transaction():
            self.pizza.create()
            self.order.create()
            self.topping1.create()

        response = self.client.get(self.list_create_uri)
        assert_that(response.status_code, is_(equal_to(200)))
        assert_that(
            response.json,
            has_entries(
                items=contains(
                    has_entries(
                        id=str(self.topping1.id),
                        pizzaId=str(self.topping1.pizza_id),
                        toppingType="ONION",
                    )
                )
            ),
        )

    def test_create(self):
        # TODO: Talk to dino about this :magic:
        with self.graph.flask.test_request_context():
            with SessionContext(self.graph), transaction():
                self.order.create()
                self.factory.create(
                    ns=None,
                    sns_producer=self.graph.sns_producer,
                    event_type=OrderEventType.OrderInitialized,
                    order_id=self.order_id,
                    customer_id=self.customer_id,
                )
                self.pizza.create()
                self.factory.create(
                    ns=None,
                    sns_producer=self.graph.sns_producer,
                    event_type=OrderEventType.PizzaCreated,
                    order_id=self.order_id,
                    customer_id=self.customer_id,
                )

        with patch.object(self.graph.topping_store, "new_object_id") as mocked:
            mocked.return_value = self.topping1.id
            response = self.client.post(
                self.list_create_uri,
                json=dict(
                    pizzaId=self.pizza_id, toppingType="CHEESE", orderId=self.order_id
                ),
            )
        assert_that(response.status_code, is_(equal_to(201)))
        assert_that(
            response.json,
            has_entries(
                id=str(self.topping1.id),
                pizzaId=str(self.pizza_id),
                toppingType="CHEESE",
                orderId=str(self.order_id),
            ),
        )

    def test_retrieve(self):

        with SessionContext(self.graph), transaction():
            self.order.create()
            self.pizza.create()
            self.topping1.create()

        response = self.client.get(self.detail_uri)

        assert_that(
            response.json,
            has_entries(
                id=str(self.topping1.id),
                pizzaId=str(self.topping1.pizza_id),
                toppingType="ONION",
            ),
        )

    def test_delete(self):
        with SessionContext(self.graph), transaction():
            self.pizza.create()
            self.order.create()
            self.topping1.create()

        response = self.client.delete(self.detail_uri)
        assert_that(response.status_code, is_(equal_to(204)))

        with SessionContext(self.graph) as session:
            assert session.session.query(Topping).get(self.topping_id) is None
