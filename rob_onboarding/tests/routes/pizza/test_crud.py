"""
Pizza CRUD routes tests.

Tests are sunny day cases under the assumption that framework conventions
handle most error conditions.

"""
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
from rob_onboarding.models.order_model import Order
from rob_onboarding.models.pizza_model import Pizza


class TestPizzaRoutes:
    def setup(self):
        self.graph = create_app(testing=True)
        self.client = self.graph.flask.test_client()
        recreate_all(self.graph)

        self.name1 = "name1"
        self.order_id = new_object_id()
        self.customer_id = new_object_id()
        self.order = Order(
            id=self.order_id, customer_id=self.customer_id
        )
        self.pizza1 = Pizza(
            id=new_object_id(), customer_id=self.customer_id, crust_type="thin", size=12,
            order_id=self.order_id,
        )

    def teardown(self):
        self.graph.postgres.dispose()

    def test_search(self):
        with SessionContext(self.graph), transaction():
            self.order.create()
            self.pizza1.create()

        uri = "/api/v1/pizza"

        response = self.client.get(uri)

        assert_that(response.status_code, is_(equal_to(200)))
        assert_that(
            response.json,
            has_entries(
                items=contains(
                    has_entries(
                        id=str(self.pizza1.id),
                        customerId=str(self.pizza1.customer_id),
                        crustType="thin",
                        size=12,
                    ),
                ),
            ),
        )

    def test_create(self):
        uri = "/api/v1/pizza"
        with SessionContext(self.graph), transaction():
            self.order.create()

        customer_id = str(new_object_id())
        with patch.object(self.graph.pizza_store, "new_object_id") as mocked:
            mocked.return_value = self.pizza1.id
            response = self.client.post(
                uri, json=dict(
                    customerId=customer_id, crustType="thin", size=12,
                    orderId=self.order_id
                ),
            )

        assert_that(response.status_code, is_(equal_to(201)))
        assert_that(
            response.json,
            has_entries(
                id=str(self.pizza1.id),
                customerId=customer_id,
                crustType="thin",
                size=12,
            ),
        )

    def test_replace_with_new(self):
        with SessionContext(self.graph), transaction():
            self.order.create()
            self.pizza1.create()
        uri = f"/api/v1/pizza/{self.pizza1.id}"
        response = self.client.put(
            uri, json=dict(size=12, customerId=self.customer_id, crustType="thin",
                           orderId=self.order_id),
        )

        assert_that(response.status_code, is_(equal_to(200)))
        assert_that(
            response.json,
            has_entries(
                id=str(self.pizza1.id),
                customerId=str(self.customer_id),
                crustType="thin",
                size=12,
                orderId=str(self.order_id),
            ),
        )

    def test_retrieve(self):
        with SessionContext(self.graph), transaction():
            self.order.create()
            self.pizza1.create()

        uri = f"/api/v1/pizza/{self.pizza1.id}"

        response = self.client.get(uri)

        assert_that(
            response.json,
            has_entries(
                id=str(self.pizza1.id),
                customerId=str(self.pizza1.customer_id),
                crustType="thin",
                size=12,
                orderId=str(self.order_id),
            ),
        )

    def test_delete(self):
        with SessionContext(self.graph), transaction():
            self.order.create()
            self.pizza1.create()

        uri = f"/api/v1/pizza/{self.pizza1.id}"

        response = self.client.delete(uri)
        assert_that(response.status_code, is_(equal_to(204)))
