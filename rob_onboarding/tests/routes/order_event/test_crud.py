from hamcrest import assert_that, is_, equal_to, has_entries, contains
from microcosm_postgres.context import SessionContext, transaction
from microcosm_postgres.identifiers import new_object_id
from microcosm_postgres.operations import recreate_all

from rob_onboarding.app import create_app
from rob_onboarding.models.order_event_model import OrderEvent


class TestOrderEventRoutes:
    list_uri = "/api/v1/orderevent"
    def setup(self):
        self.graph = create_app(testing=True)
        self.client = self.graph.flask.test_client()
        recreate_all(self.graph)

        self.order_event_id = new_object_id()
        self.order_event = OrderEvent(
            id=self.order_event_id, order_id=new_object_id(),
            event_type='OrderInitialized'
        )
        self.detail_uri = f"/api/v1/orderevent/{self.order_event_id}"

    def teardown(self):
        self.graph.postgres.dispose()

    def test_search(self):
        with SessionContext(self.graph), transaction():
            self.order_event.create()

        response = self.client.get(self.list_uri)
        assert_that(response.status_code, is_(equal_to(200)))
        assert_that(
            response.json,
            has_entries(
                items=contains(
                    has_entries(
                        id=str(self.order_event_id.id),
                        orderId=str(self.order_event.order_id),
                    )
                )
            )
        )

    def test_retrieve(self):
        with SessionContext(self.graph), transaction():
            self.order_event.create()

        response = self.client.get(self.detail_uri)

        assert_that(
            response.json,
            has_entries(
                id=str(self.order_event.id),
                orderId=str(self.order_event.order_id),
            ),
        )
