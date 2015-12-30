from schematics.models import Model
from schematics.types import StringType, IntType
from schematics.types.base import BooleanType
from schematics.types.compound import ListType, ModelType


class SFBaseValidator(Model):
    def __init__(self, raw_data=None, **kwargs):
        self.json = raw_data
        super(SFBaseValidator, self).__init__(raw_data=raw_data, **kwargs)


# TODO can we abstract away the 'ok' check to the validator?
class Symbol(SFBaseValidator):
    name = StringType(required=True)
    symbol = StringType(required=True)


class Stocks(SFBaseValidator):
    symbols = ListType(ModelType(Symbol))


class BidOrAsk(SFBaseValidator):
    price = IntType(required=True)
    qty = IntType(required=True)
    isBuy = BooleanType(required=True)


class Orderbook(SFBaseValidator):
    venue = StringType(required=True)
    symbol = StringType(required=True)
    bids = ListType(ModelType(BidOrAsk))
    asks = ListType(ModelType(BidOrAsk))
    ts = StringType(required=True)


class Fills(SFBaseValidator):
    price = IntType(required=True)
    qty = IntType(required=True)
    ts = StringType(required=True)


class Order(SFBaseValidator):
    symbol = StringType(required=True)
    venue = StringType(required=True)
    direction = StringType(required=True)
    originalQty = IntType(required=True)
    qty = IntType(required=True)
    price = IntType(required=True)
    type = StringType(required=True)
    id = IntType(required=True)
    account = StringType(required=True)
    ts = StringType(required=True)
    fills = ListType(ModelType(Fills))
    totalFilled = IntType(required=True)
    open = BooleanType(required=True)

    def __init__(self, raw_data=None, **kwargs):
        if isinstance(raw_data, dict) and 'orderType' in raw_data:
            raw_data['type'] = raw_data['orderType']
        super(Order, self).__init__(raw_data=raw_data, **kwargs)


class Orders(SFBaseValidator):
    venue = StringType(required=True)
    orders = ListType(Order)


class Quote(SFBaseValidator):
    symbol = StringType(required=True)
    venue = StringType(required=True)
    bid = IntType(required=True)
    ask = IntType(required=True)
    bidSize = IntType(required=True)
    askSize = IntType(required=True)
    bidDepth = IntType(required=True)
    askDepth = IntType(required=True)
    last = IntType(required=True)
    lastSize = IntType(required=True)
    lastTrade = StringType(required=True)
    quoteTime = StringType(required=True)
