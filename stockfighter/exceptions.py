from pprint import pformat


class SFBaseException(Exception):
    def __init__(self, sc, json=None):
        self.status_code = sc
        self.json = json

    def __str__(self):
        return 'status code: {}\nresponse: {}'.format(self.status_code, pformat(self.json))


class HealthcheckFailed(SFBaseException):
    pass


class UnknownExchange(SFBaseException):
    def __str__(self):
        return 'status code: {}'.format(self.status_code)


class BadRequest(SFBaseException):
    pass


class Unauthorized(SFBaseException):
    pass


class SyntaxError_(Exception):
    def __init__(self, tokens, idx):
        self.tokens = tokens
        self.idx = idx

    def __str__(self):
        return (
            ' ' * len(''.join(self.tokens[:self.idx])) +
            '^' + ' ' * len(''.join(self.tokens[self.idx:]))
        )
