from marshmallow import Schema, fields
from microcosm_flask.linking import Link, Links
from microcosm_flask.namespaces import Namespace
from microcosm_flask.operations import Operation
from microcosm_flask.paging import PageSchema

from rob_onboarding.models.pizza_model import Pizza
from rob_onboarding.models.topping_model import Topping


class NewToppingSchema(Schema):
    pizza_id = fields.UUID(required=True, data_key='pizzaId')
    topping_type = fields.String(required=True, data_key='toppingType')


class ToppingSchema(Schema):
    id = fields.UUID(required=True)
    pizza_id = fields.UUID(required=True, data_key='pizzaId')
    topping_type = fields.String(required=True, data_key='toppingType')
    _links = fields.Method('get_links', dump_only=True)

    def get_links(self, obj):
        links = Links()
        links['self'] = Link.for_(
            Operation.Retrieve,
            Namespace(
                subject=Topping,
                version='v1',
            ), topping_id=obj.id
        )
        links['parent:pizza'] = Link.for_(
            Operation.Search,
            Namespace(
                subject=Pizza,
                version='v1'
            ),
            id=obj.pizza_id
        )
        return links.to_dict()


class SearchToppingSchema(PageSchema):
    pizza_id = fields.UUID(data_key='pizzaId')
