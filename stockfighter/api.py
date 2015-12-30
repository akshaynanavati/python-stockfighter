import requests

import config
from constants import (
    SF_API_BASE,
    TEST_EXCHANGE,
    SF_AUTH_HEADER_KEY,
    MARKET_ORDER,
    TEST_STOCK,
)
from exceptions import (
    HealthcheckFailed,
    SFBaseException,
    UnknownExchange,
    BadRequest,
    Unauthorized,
)
from validators import (
    Stocks,
    Orderbook,
    Order,
    Orders,
    Quote,
)


def healthcheck(venue=None):
    '''
    :param venue: a string representing the venue to healthcheck. If None or unspecified, \
        this function will check the health of the overall stockfighter api
    Raises an exception if the healthcheck fails i.e. the stockfighter servers
    are down.
    '''
    if venue is None:
        path = '/heartbeat'
    else:
        path = '/venues/{}/heartbeat'

    response = _make_request(path)
    json = response.json()
    if response.status_code != 200 or not json['ok']:
        raise HealthcheckFailed(response.status_code, json)


def get_stocks(exchange=TEST_EXCHANGE):
    '''
    Returns a list of all stocks traded on the given exchange where each "stock" is a
    dict with two keys: name, symbol.

    TODO: this request can be cached.
    '''
    sc, json = _make_request('/venues/{}/stocks'.format(exchange))

    if sc == 404:
        raise UnknownExchange(404)

    return Stocks(json)


def get_orderbook(exchange=TEST_EXCHANGE, stock=TEST_STOCK):
    sc, json = _make_request('/venues/{}/stocks/{}'.format(exchange, stock))
    if sc == 404:
        raise BadRequest(sc, json)
    return Orderbook(json, strict=False)


def get_quote(exchange=TEST_EXCHANGE, stock=TEST_STOCK):
    sc, json = _make_request('/venues/{}/stocks/{}/quote'.format(exchange, stock))
    if sc == 404:
        raise BadRequest(sc, json)
    return Quote(json)


def order_status(id_, exchange=TEST_EXCHANGE, stock=TEST_STOCK):
    sc, json = _make_request('/venues/{}/stocks/{}/orders/{}'.format(exchange, stock, id_))
    if sc == 401:
        raise Unauthorized(sc, json)
    return Order(json)


def delete_order(id_, exchange=TEST_EXCHANGE, stock=TEST_STOCK):
    sc, json = _make_request(
        '/venues/{}/stocks/{}/orders/{}'.format(exchange, stock, id_), type_='delete'
    )
    if sc == 401:
        raise Unauthorized(sc, json)
    return Order(json)


def all_orders(exchange=TEST_EXCHANGE, stock=None):
    if stock is None:
        path = '/venues/{}/accounts/{}/orders'.format(exchange, config.get('account'))
    else:
        path = '/venues/{}/accounts/{account}/stocks/{}/orders'.format(
            exchange,
            config.get('account'),
            stock,
        )
    _, json = _make_request(path)
    return Orders(json)


def buy_stock(quantity, **kwargs):
    return trade_stock(quantity, 'buy', **kwargs)


def sell_stock(quantity, **kwargs):
    return trade_stock(quantity, 'sell', **kwargs)


def trade_stock(
    quantity,
    direction,
    exchange=TEST_EXCHANGE,
    stock=TEST_STOCK,
    price=None,
    order_type=MARKET_ORDER,
):
    if price is None:
        order_type = MARKET_ORDER
        price = 0
    else:
        price = int(price * 100)

    sc, json = _make_request(
        path='/venues/{}/stocks/{}/orders'.format(exchange, stock),
        type_='post',
        data={
            'account': config.get('account'),
            'venue': exchange,
            'stock': stock,
            'price': price,
            'qty': quantity,
            'direction': direction,
            'orderType': order_type,
        },
    )

    if sc != 200:
        raise BadRequest(sc, json)

    return Order(json, strict=False)


def _make_request(path, type_='get', data=None, headers=None):
    if headers is None:
        headers = {}

    response = getattr(requests, type_)(
        '{}{}'.format(SF_API_BASE, path),
        headers=dict({
            SF_AUTH_HEADER_KEY: API_KEY,
        }, **headers),
        json=data,
    )

    sc = response.status_code
    json = response.json()
    if sc == 200 and not json['ok']:
        raise SFBaseException(sc, json)
    return sc, json
