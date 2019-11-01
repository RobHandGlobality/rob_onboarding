"""
Topping persistence tests.

"""
from hamcrest import assert_that, equal_to, is_
from microcosm_postgres.context import SessionContext, transaction
from microcosm_postgres.identifiers import new_object_id

from rob_onboarding.app import create_app
from rob_onboarding.models.topping_model import Topping


class TestTopping:
    def setup(self):
        self.graph = create_app(testing=True)
        self.topping_store = self.graph.topping_store

        self.topping_type = "ONION"
        self.pizza_id = new_object_id()

        self.context = SessionContext(self.graph)
        self.context.recreate_all()
        self.context.open()

    def teardown(self):
        self.context.close()
        self.graph.postgres.dispose()

    def test_create(self):
        """
        Topping can be persisted.

        """
        new_topping = Topping(pizza_id=new_object_id(), topping_type=self.topping_type,)

        with transaction():
            self.topping_store.create(new_topping)

        retrieved_topping = self.topping_store.retrieve(new_topping.id)
        assert_that(retrieved_topping, is_(equal_to(new_topping)))
