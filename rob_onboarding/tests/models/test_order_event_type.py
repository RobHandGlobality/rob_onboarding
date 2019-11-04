from hamcrest import assert_that, is_, equal_to

from rob_onboarding.models.order_event_type import OrderEventType


class TestOrderEventType:

    def test_initial_state(self):
        state = set()
        for event_type in OrderEventType:
            is_start = event_type == OrderEventType.OrderInitialized
            assert_that(event_type.may_transition(state), is_(equal_to(is_start)))

    def test_basic_pizza_order_states_transitions(self):
        event_types = (
            OrderEventType.OrderInitialized,
            OrderEventType.PizzaCreated,
            OrderEventType.PizzaToppingAdded,
            OrderEventType.PizzaCustomizationFinished,
            OrderEventType.OrderDeliveryDetailsAdded,
            OrderEventType.OrderSubmitted,
            OrderEventType.OrderSatisfied,
        )
        state = set()
        for event_type in event_types:
            assert_that(event_type.may_transition(state), is_(equal_to(True)))
            state = set(event_type.accumulate_state(state))

    def test_must_add_at_least_one_topping_to_progress_flow(self):
        initial_state = set(OrderEventType.OrderInitialized.accumulate_state(set()))
        pizza_added = set(OrderEventType.PizzaCreated.accumulate_state(initial_state))
        assert_that(
            OrderEventType.PizzaCustomizationFinished.may_transition(pizza_added),
            is_(equal_to(False))
        )

    def test_topping_added_flow(self):
        initial_state = set(OrderEventType.OrderInitialized.accumulate_state(set()))
        pizza_added = set(OrderEventType.PizzaCreated.accumulate_state(initial_state))
        topping_added = set(OrderEventType.PizzaToppingAdded.accumulate_state(pizza_added))
        assert_that(
            OrderEventType.PizzaCustomizationFinished.may_transition(topping_added),
            is_(equal_to(True)),
        )

    def test_adding_multiple_toppings_is_allowed(self):
        initial_state = set(OrderEventType.OrderInitialized.accumulate_state(set()))
        pizza_added = set(OrderEventType.PizzaCreated.accumulate_state(initial_state))
        topping_added_1 = set(OrderEventType.PizzaToppingAdded.accumulate_state(pizza_added))
        topping_added_2 = set(OrderEventType.PizzaToppingAdded.accumulate_state(topping_added_1))
        assert_that(
            OrderEventType.PizzaToppingAdded.may_transition(topping_added_2),
            is_(equal_to(True)),
        )
