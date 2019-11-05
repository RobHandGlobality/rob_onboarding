from microcosm_eventsource.event_types import EventType, event_info
from microcosm_eventsource.transitioning import any_of, event, nothing


class OrderEventType(EventType):
    """
        Order event type. Models the user journey through specifying an order
        for a pizza as described here:
        https://globality.atlassian.net/wiki/spaces/GLOB/pages/917733426/Product+Spec+Ordering+a+Pizza

    """

    # NB: Our state machines always start with an initial event
    OrderInitialized = event_info(follows=nothing(),)

    PizzaCreated = event_info(
        follows=any_of("OrderInitialized", "PizzaCustomizationFinished",),
    )

    PizzaToppingAdded = event_info(
        follows=any_of("PizzaCreated", "PizzaToppingAdded",),
    )

    PizzaCustomizationFinished = event_info(follows=any_of("PizzaToppingAdded",),)

    OrderDeliveryDetailsAdded = event_info(follows=event("PizzaCustomizationFinished"),)

    OrderSubmitted = event_info(follows=event("OrderDeliveryDetailsAdded"),)

    OrderSatisfied = event_info(follows=event("OrderSubmitted"),)

    OrderFulfilled = event_info(follows=event("OrderSubmitted"),)
