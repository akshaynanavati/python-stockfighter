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

    Raises :py:exception:`HealthcheckFailed` if the healthcheck fails i.e. the \
    stockfighter servers are down.
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
    :param exchange: a string with the exchange name (case sesitive) from which to retrieve \
        all stocks. Defaults to :py:data:`TEST_EXCHANGE`.

    :rtype: :py:class:`Stocks`
    :return: The deserialized json response as a schematics object

    Gets all the stocks traded on an exchange.
    '''
    sc, json = _make_request('/venues/{}/stocks'.format(exchange))

    if sc == 404:
        raise UnknownExchange(404)

    return Stocks(json)


def get_orderbook(exchange=TEST_EXCHANGE, stock=TEST_STOCK):
    '''
    :param exchange: a string with the exchange name (case sesitive). \
        Defaults to :py:data:`TEST_EXCHANGE`.
    :param stock: a string with the stock name (case sensitive) which must be traded in the \
        exchange. Defaults to :py:data:`TEST_STOCK`.

    :rtype: :py:class:`Orderbook`
    :return: The deserialized json response as a schematics object

    Retrieves the orderbook for a given stock on an exchange.
    '''
    sc, json = _make_request('/venues/{}/stocks/{}'.format(exchange, stock))
    if sc == 404:
        raise BadRequest(sc, json)
    return Orderbook(json, strict=False)


def get_quote(exchange=TEST_EXCHANGE, stock=TEST_STOCK):
    '''
    :param exchange: a string with the exchange name (case sesitive). \
        Defaults to :py:data:`TEST_EXCHANGE`.
    :param stock: a string with the stock name (case sensitive) which must be traded in the \
        exchange. Defaults to :py:data:`TEST_STOCK`.

    :rtype: :py:class:`Quote`
    :return: The deserialized json response as a schematics object

    Gets a quote of the latest known order for a given stock on an exchange.
    '''
    sc, json = _make_request('/venues/{}/stocks/{}/quote'.format(exchange, stock))
    if sc == 404:
        raise BadRequest(sc, json)
    return Quote(json)


def order_status(id_, exchange=TEST_EXCHANGE, stock=TEST_STOCK):
    '''
    :param id_: the order id
    :param exchange: a string with the exchange name (case sesitive). \
        Defaults to :py:data:`TEST_EXCHANGE`.
    :param stock: a string with the stock name (case sensitive) which must be traded in the \
        exchange. Defaults to :py:data:`TEST_STOCK`.

    :rtype: :py:class:`Order`
    :return: The deserialized json response as a schematics object

    Retrieves the order status for the specified order on the given exchange.
    '''
    sc, json = _make_request('/venues/{}/stocks/{}/orders/{}'.format(exchange, stock, id_))
    if sc == 401:
        raise Unauthorized(sc, json)
    return Order(json)


def delete_order(id_, exchange=TEST_EXCHANGE, stock=TEST_STOCK):
    '''
    :param id_: the order id
    :param exchange: a string with the exchange name (case sesitive). \
        Defaults to :py:data:`TEST_EXCHANGE`.
    :param stock: a string with the stock name (case sensitive) which must be traded in the \
        exchange. Defaults to :py:data:`TEST_STOCK`.

    :rtype: :py:class:`Order`
    :return: The deserialized json response as a schematics object

    Deletes the specified order.
    '''
    sc, json = _make_request(
        '/venues/{}/stocks/{}/orders/{}'.format(exchange, stock, id_), type_='delete'
    )
    if sc == 401:
        raise Unauthorized(sc, json)
    return Order(json)


def all_orders(exchange=TEST_EXCHANGE, stock=None):
    '''
    :param exchange: a string with the exchange name (case sesitive). \
        Defaults to :py:data:`TEST_EXCHANGE`.
    :param stock: a string with the stock name (case sensitive) which must be traded in the \
        exchange. Defaults to ``None``.

    :rtype: :py:class:`Orders`
    :return: The deserialized json response as a schematics object

    Returns all orders on a given exchange. If specified, narrows down orders to the given stock.
    '''
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
    '''
    :param quantity: the number of shares to buy
    :param exchange: a string with the exchange name (case sesitive). \
        Defaults to :py:data:`TEST_EXCHANGE`.
    :param stock: a string with the stock name (case sensitive) which must be traded in the \
        exchange. Defaults to :py:data:`TEST_STOCK`.
    :param price: The price to buy at. Defaults to ``None``. If none or unspecified, the order \
        becomes a market order.
    :param order_type: The type of order. Should be one of :py:data:`MARKET_ORDER`, \
        :py:data:`LIMIT_ORDER`, :py:data:`FILL_OR_KILL_ORDER`, :py:data:`IMMEDIATE_OR_CANCEL`. \
        Defaults to :py:data:`MARKET_ORDER`

    :rtype: :py:class:`Order`
    :return: The deserialized json response as a schematics object

    Executes a buy order and returns the result.
    '''
    return trade_stock(quantity, 'buy', **kwargs)


def sell_stock(quantity, **kwargs):
    '''
    :param quantity: the number of shares to sell
    :param exchange: a string with the exchange name (case sesitive). \
        Defaults to :py:data:`TEST_EXCHANGE`.
    :param stock: a string with the stock name (case sensitive) which must be traded in the \
        exchange. Defaults to :py:data:`TEST_STOCK`.
    :param price: The price to buy at. Defaults to ``None``. If none or unspecified, the order \
        becomes a market order.
    :param order_type: The type of order. Should be one of :py:data:`MARKET_ORDER`, \
        :py:data:`LIMIT_ORDER`, :py:data:`FILL_OR_KILL_ORDER`, :py:data:`IMMEDIATE_OR_CANCEL`. \
        Defaults to :py:data:`MARKET_ORDER`

    :rtype: :py:class:`Order`
    :return: The deserialized json response as a schematics object

    Executes a sell order and returns the result.
    '''
    return trade_stock(quantity, 'sell', **kwargs)


def trade_stock(
    quantity,
    direction,
    exchange=TEST_EXCHANGE,
    stock=TEST_STOCK,
    price=None,
    order_type=MARKET_ORDER,
):
    '''
    :param quantity: the number of shares to buy or sell
    :param direction: either ``'buy'`` or ``'sell'``
    :param exchange: a string with the exchange name (case sesitive). \
        Defaults to :py:data:`TEST_EXCHANGE`.
    :param stock: a string with the stock name (case sensitive) which must be traded in the \
        exchange. Defaults to :py:data:`TEST_STOCK`.
    :param price: The price to buy at. Defaults to ``None``. If none or unspecified, the order \
        becomes a market order.
    :param order_type: The type of order. Should be one of :py:data:`MARKET_ORDER`, \
        :py:data:`LIMIT_ORDER`, :py:data:`FILL_OR_KILL_ORDER`, :py:data:`IMMEDIATE_OR_CANCEL`. \
        Defaults to :py:data:`MARKET_ORDER`

    :rtype: :py:class:`Order`
    :return: The deserialized json response as a schematics object

    Executes a buy or sell order and returns the result.
    '''
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
    '''
    :param path: The path to the stockfighter API
    :param type_: HTTP request type in lowercase i.e. ``'get'``, ``'post'``, ``'delete'`` etc.
    :param data: a python dict which will be serialized and sent as json
    :param headers: headers to send along with the request

    :rtype: (integer, dictionary)
    :return: a tuple of status code and deserialized json response as a python dict

    Makes the specified request to the stockfighter api. If ``'ok'`` is not ``True`` in the \
    response, this will raise :py:exception:`SFBaseException`.
    '''
    if headers is None:
        headers = {}

    response = getattr(requests, type_)(
        '{}{}'.format(SF_API_BASE, path),
        headers=dict({
            SF_AUTH_HEADER_KEY: config.get('api_key'),
        }, **headers),
        json=data,
    )

    sc = response.status_code
    json = response.json()
    if sc == 200 and not json['ok']:
        raise SFBaseException(sc, json)
    return sc, json
