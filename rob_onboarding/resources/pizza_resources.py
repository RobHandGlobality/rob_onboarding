"""
Pizza resources.

"""
from marshmallow import Schema, fields
from microcosm_flask.linking import Link, Links
from microcosm_flask.namespaces import Namespace
from microcosm_flask.operations import Operation
from microcosm_flask.paging import PageSchema

from rob_onboarding.models.pizza_model import Pizza


class NewPizzaSchema(Schema):
    customer_id = fields.UUID(
        required=True, data_key='customerId'
    )
    size = fields.Integer(required=False, default=10)
    crust_type = fields.String(required=False, data_key='crustType', default='thin')


class PizzaSchema(NewPizzaSchema):
    id = fields.UUID(
        required=True,
    )
    _links = fields.Method(
        "get_links",
        dump_only=True,
    )

    def get_links(self, obj):
        links = Links()
        links["self"] = Link.for_(
            Operation.Retrieve,
            Namespace(
                subject=Pizza,
                version="v1",
            ),
            pizza_id=obj.id,
        )
        return links.to_dict()


class SearchPizzaSchema(PageSchema):
    order = fields.String()
    id = fields.String()
