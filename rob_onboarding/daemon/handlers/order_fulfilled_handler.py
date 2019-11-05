from urllib.parse import urljoin

import requests
from microcosm.decorators import binding
from microcosm_logging.decorators import logger
from microcosm_pubsub.chain import Chain, assign, extracts
from microcosm_pubsub.conventions import created
from microcosm_pubsub.decorators import handles
from microcosm_pubsub.errors import Nack, SkipMessage
from microcosm_pubsub.handlers import ChainURIHandler

from rob_onboarding.models.order_event_type import OrderEventType


@binding("order_fulfilled_handler")
@handles(created("DeliveryEvent.PizzaDelivered"))
@logger
class OrderFulfilledHandler(ChainURIHandler):
    def __init__(self, graph):
        super().__init__(graph)
        self.server_uri = "http://localhost:5000"

    @property
    def resource_name(self):
        return "delivery_event"

    def get_chain(self):
        return Chain(
            assign("delivery_event.orderId").to("order_id"),
            self.extract_order,
            assign("order.customerId").to("customer_id"),
            self.extract_latest_order_event,
            assign("latest_order_event.eventType").to("last_event_type"),
            self.assert_order_ready_for_fulfillment,
            self.set_order_fulfilled_event,
        )

    @extracts("order")
    def extract_order(self, order_id):
        response = requests.get(urljoin(self.server_uri, f"api/v1/order/{order_id}"))
        response.raise_for_status()
        return response.json()

    @extracts("latest_order_event")
    def extract_latest_order_event(self, order_id):
        response = requests.get(
            urljoin(self.server_uri, f"api/v1/order_event?orderId={order_id}")
        )
        response.raise_for_status()
        return response.json()["items"][0]

    def assert_order_ready_for_fulfillment(self, last_event_type, order_id):
        # Check if order in correct state
        if last_event_type == str(OrderEventType.OrderSubmitted):
            return

        # Order is already Fulfilled, so skip
        if last_event_type == str(OrderEventType.OrderFulfilled):
            raise SkipMessage(f"Order {order_id} already fulfilled")

        raise Nack(4)  # TODO Move to a config var see dinos PR

    def set_order_fulfilled_event(self, order_id, customer_id):
        response = requests.post(
            url=urljoin(self.server_uri, "api/v1/order_event"),
            json=dict(
                # customerId=str(customer_id),
                orderId=str(order_id),
                eventType=str(OrderEventType.OrderFulfilled),
            ),
        )
        response.raise_for_status()
        return True
