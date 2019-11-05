"""
OrderEvent resources.

"""
from marshmallow import Schema, fields
from microcosm_flask.fields import EnumField
from microcosm_flask.linking import Link, Links
from microcosm_flask.namespaces import Namespace
from microcosm_flask.operations import Operation
from microcosm_flask.paging import PageSchema

from rob_onboarding.models.order_event_model import OrderEvent
from rob_onboarding.models.order_event_type import OrderEventType


class NewOrderEventSchema(Schema):
    # TODO Restore when migration fixed
    # customer_id = fields.UUID(required=True, data_key='customerId')
    order_id = fields.UUID(required=True, data_key="orderId")
    event_type = EnumField(OrderEventType, required=True, data_key="eventType")


class OrderEventSchema(NewOrderEventSchema):
    id = fields.UUID(required=True,)
    _links = fields.Method("get_links", dump_only=True,)

    def get_links(self, obj):
        links = Links()
        links["self"] = Link.for_(
            Operation.Retrieve,
            Namespace(subject=OrderEvent, version="v1",),
            order_event_id=obj.id,
        )

        return links.to_dict()


class SearchOrderEventSchema(PageSchema):
    orderId = fields.String()
