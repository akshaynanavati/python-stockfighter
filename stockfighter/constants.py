# API Constants
SF_API_BASE = 'https://api.stockfighter.io/ob/api'
SF_AUTH_HEADER_KEY = 'X-Starfighter-Authorization'

# Test values
TEST_EXCHANGE = 'TESTEX'
TEST_STOCK = 'FOOBAR'
TEST_ACCOUNT = 'EXB123456'

# Order Types
MARKET_ORDER = 'market'  # buys stock at any price
LIMIT_ORDER = 'limit'  # shares are bought for at most specified price (vice versa for sell)
FILL_OR_KILL_ORDER = 'fill-or-kill'  # get exactly as many shares as you asked for or none
IMMEDIATE_OR_CANCEL = 'immediate-or-cancel'  # like fok but you could get <= specified ammount
