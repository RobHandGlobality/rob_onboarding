from unittest.mock import MagicMock, patch

from contextdecorator import contextmanager
from hamcrest import (
    assert_that,
    calling,
    equal_to,
    is_,
    raises,
)
from microcosm_postgres.identifiers import new_object_id
from microcosm_pubsub.errors import SkipMessage

from rob_onboarding.daemon.main import RobOnboardingOrdersDaemon
from rob_onboarding.models.order_event_type import OrderEventType


@contextmanager
def mock_handler_actions():
    with patch(
        "rob_onboarding.daemon.handlers.order_fulfilled_handler.requests.get"
    ) as mock_get_resources:
        with patch(
            "rob_onboarding.daemon.handlers.order_fulfilled_handler.requests.post"
        ) as mock_create_event:
            yield mock_get_resources, mock_create_event


class TestOrderFulfilledHandler:
    def setup(self):
        self.graph = RobOnboardingOrdersDaemon.create_for_testing().graph
        self.handler = self.graph.order_fulfilled_handler

        self.customer_id = new_object_id()
        self.delivery_event_id = new_object_id()
        self.order_id = new_object_id()
        self.delivery_event_type = "DeliveryCompleted"
        self.message = dict(
            uri=f"https://deliveries.dev.globaltiy.io/api/v1/delivery_event/{self.delivery_event_id}"
        )
        self.delivery_event = dict(
            id=self.delivery_event_id,
            orderId=self.order_id,
            eventType=self.delivery_event_type,
        )
        self.order = MagicMock(
            json=MagicMock(return_value=dict(customerId=self.customer_id)),
            raise_for_status=MagicMock(),
        )
        self.order_event = MagicMock(
            json=MagicMock(
                return_value=dict(
                    items=[dict(eventType=str(OrderEventType.OrderSubmitted))]
                )
            )
        )

    def test_base_case(self):
        with patch.object(self.handler, "get_resource") as mocked_get_delivery_event:
            with mock_handler_actions() as (mock_get, mock_post):
                mocked_get_delivery_event.return_value = self.delivery_event
                mock_get.side_effect = [
                    self.order,
                    self.order_event,
                ]

                assert_that(self.handler(self.message), is_(equal_to(True)))
                # Once to get the order, once to get the order_event
                assert_that(mock_get.call_count, equal_to(2))
                mock_post.assert_called_once_with(
                    url="http://localhost:5000/api/v1/order_event",
                    json=dict(
                        orderId=str(self.order_id),
                        eventType=OrderEventType.OrderFulfilled.name,
                    ),
                )

    def test_skipping_if_already_fulfilled(self):
        fulfilled_event = MagicMock(
            json=MagicMock(
                return_value=dict(
                    items=[dict(eventType=str(OrderEventType.OrderFulfilled))]
                )
            )
        )
        with patch.object(self.handler, "get_resource") as mocked_get_delivery_event:
            with mock_handler_actions() as (mock_get, mock_post):
                mocked_get_delivery_event.return_value = self.delivery_event
                mock_get.side_effect = [
                    self.order,
                    fulfilled_event,
                ]
                assert_that(
                    calling(self.handler).with_args(self.message), raises(SkipMessage),
                )
