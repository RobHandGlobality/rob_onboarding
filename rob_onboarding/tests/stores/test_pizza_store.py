"""
Pizza persistence tests.

Tests cover model-specific constraints under the assumption that framework conventions
handle most boilerplate.

"""
from hamcrest import (
    assert_that,
    calling,
    equal_to,
    is_,
    raises,
)
from microcosm_postgres.context import SessionContext, transaction
from microcosm_postgres.errors import DuplicateModelError

from rob_onboarding.app import create_app
from rob_onboarding.models.pizza_model import Pizza


class TestPizza:

    def setup(self):
        self.graph = create_app(testing=True)
        self.pizza_store = self.graph.pizza_store

        self.name = "NAME"

        self.context = SessionContext(self.graph)
        self.context.recreate_all()
        self.context.open()

    def teardown(self):
        self.context.close()
        self.graph.postgres.dispose()

    def test_create(self):
        """
        Examples can be persisted.

        """
        new_pizza = Pizza(
            customer_id=1,
            crust_type='thin',
            size=10
        )

        with transaction():
            self.pizza_store.create(new_pizza)

        retrieved_pizza = self.pizza_store.retrieve(new_pizza.id)
        assert_that(retrieved_pizza, is_(equal_to(new_pizza)))
