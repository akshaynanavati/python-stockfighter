import json

from constants import TEST_ACCOUNT

_retriever = {
    'account': TEST_ACCOUNT,
}


def init(account_number, key_file='~/.stockfighter/keys.json'):
    _retriever['account'] = account_number
    if 'api_key' not in _retriever:
        with open(key_file) as f:
            _retriever['api_key'] = json.load(f)['api_key']


def reset():
    _retriever['account'] = TEST_ACCOUNT


def get(key):
    return _retriever[key]


def set_(key, value):
    if key in _retriever:
        raise ValueError('Key {} already in config object'.format(key))

    _retriever[key] = value
