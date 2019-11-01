"""
Pizza persistence tests.

Tests cover model-specific constraints under the assumption that framework conventions
handle most boilerplate.

"""
from hamcrest import assert_that, equal_to, is_
from microcosm_postgres.context import SessionContext, transaction
from microcosm_postgres.identifiers import new_object_id

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
        Pizza can be persisted.

        """
        new_pizza = Pizza(customer_id=new_object_id(), crust_type="thin", size=10)

        with transaction():
            self.pizza_store.create(new_pizza)

        retrieved_pizza = self.pizza_store.retrieve(new_pizza.id)
        assert_that(retrieved_pizza, is_(equal_to(new_pizza)))
