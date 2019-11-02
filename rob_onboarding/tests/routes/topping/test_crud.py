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
from rob_onboarding.models.topping_model import Topping


class TestToppingRoutes:
    list_create_uri = "/api/v1/topping"

    def setup(self):
        self.graph = create_app(testing=True)
        self.client = self.graph.flask.test_client()
        recreate_all(self.graph)

        self.topping_id = new_object_id()
        self.topping1 = Topping(
            id=self.topping_id, pizza_id=new_object_id(),
            topping_type='ONION'
        )
        self.detail_uri = f"/api/v1/topping/{self.topping1.id}"

    def teardown(self):
        self.graph.postgres.dispose()

    def test_search(self):
        with SessionContext(self.graph), transaction():
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
                        toppingType='ONION'
                    )
                )
            )
        )

    def test_create(self):
        pizza_id = str(new_object_id())
        with patch.object(self.graph.topping_store, "new_object_id") as mocked:
            mocked.return_value = self.topping1.id
            response = self.client.post(
                self.list_create_uri, json=dict(pizzaId=pizza_id, toppingType='CHEESE')
            )
        assert_that(response.status_code, is_(equal_to(201)))
        assert_that(
            response.json,
            has_entries(
                id=str(self.topping1.id),
                pizzaId=str(pizza_id),
                toppingType='CHEESE'
            )
        )

    def test_retrieve(self):
        with SessionContext(self.graph), transaction():
            self.topping1.create()

        response = self.client.get(self.detail_uri)

        assert_that(
            response.json,
            has_entries(
                id=str(self.topping1.id),
                pizzaId=str(self.topping1.pizza_id),
                toppingType='ONION'
            ),
        )

    def test_delete(self):
        with SessionContext(self.graph), transaction():
            self.topping1.create()

        response = self.client.delete(self.detail_uri)
        assert_that(response.status_code, is_(equal_to(204)))

        with SessionContext(self.graph) as session:
            assert session.session.query(Topping).get(self.topping_id) is None
