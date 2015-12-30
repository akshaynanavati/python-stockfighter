#!/usr/bin/env
import os
import sys
if __name__ == '__main__':
    sys.path.append(os.getcwd())

from pprint import pprint

from lib import config
from lib.api import (
    get_orderbook,
    trade_stock,
)
from lib.exceptions import (
    SFBaseException,
    SyntaxError_,
)


def execute_statement(stmt):
    idx = 0
    tokens = stmt.split(' ')
    try:
        if tokens[idx] == 'buy' or tokens[idx] == 'sell':
            # {buy, sell} <order_type> <int> shares of <exchange>:<stock> at <price>
            kwargs = {}
            kwargs['direction'] = tokens[idx]
            idx += 1
            kwargs['order_type'] = tokens[idx]
            idx += 1
            kwargs['quantity'] = int(tokens[idx])
            idx += 3
            kwargs['exchange'], kwargs['stock'] = tokens[idx].split(':')
            idx += 2
            kwargs['price'] = float(tokens[idx])
            print 'submitting order...',
            order = trade_stock(**kwargs)
            print 'submitted:'
            pprint(order.json)
        elif tokens[idx] == 'status':
            # status <order_id> <exchange>:<stock>
            pass
        elif tokens[idx] == 'orderbook':
            idx += 1
            exchange, stock = tokens[idx].split(':')
            order = get_orderbook(exchange=exchange, stock=stock)
            pprint(order.json)
        elif tokens[idx] == 'set':
            idx += 1
            assert tokens[idx] == 'account'
            idx += 1
            config.init(tokens[idx])
        else:
            # TODO fill in any other operators
            raise Exception()
    except SFBaseException:
        raise
    except Exception:
        raise SyntaxError_(tokens, idx)


if __name__ == '__main__':
    print 'entering while'
    while True:
        print 'in while'
        try:
            ps1 = '{}> '.format(config.get('account'))
            execute_statement(raw_input(ps1))
        except SyntaxError_ as e:
            print 'Syntax Error:'
            print e
        except SFBaseException as e:
            print 'SF API Error:'
            print e
