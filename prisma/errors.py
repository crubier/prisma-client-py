from typing import Any, Optional


__all__ = (
    'PrismaError',
    'DataError',
    'UniqueViolationError',
    'MissingRequiredValueError',
    'RawQueryError',
    'TableNotFoundError',
    'RecordNotFoundError',
    'HTTPClientClosedError',
    'ClientNotConnectedError',
    'PluginError',
    'PluginMissingRequiredHookError',
)


class PrismaError(Exception):
    pass


class ClientNotConnectedError(PrismaError):
    def __init__(self) -> None:
        super().__init__(
            'Client is not connected to the query engine, '
            'you must `await client.connect()` before attempting to query data.'
        )


class HTTPClientClosedError(PrismaError):
    def __init__(self) -> None:
        super().__init__('Cannot make a request from a closed client.')


class DataError(PrismaError):
    def __init__(self, data: Any, *, message: Optional[str] = None):
        self.data = data

        user_facing_error = data.get('user_facing_error', {})
        self.code = user_facing_error.get('error_code')
        self.meta = user_facing_error.get('meta')

        message = message or user_facing_error.get('message')
        super().__init__(message or 'An error occurred while processing data.')


class UniqueViolationError(DataError):
    pass


class MissingRequiredValueError(DataError):
    pass


class RawQueryError(DataError):
    def __init__(self, data: Any):
        try:
            super().__init__(data, message=data['user_facing_error']['meta']['message'])
        except KeyError:
            super().__init__(data)


class TableNotFoundError(DataError):
    def __init__(self, data: Any):
        super().__init__(data)
        self.table = self.meta.get('table')  # type: Optional[str]


class RecordNotFoundError(DataError):
    pass


class PluginError(PrismaError):
    pass


class PluginMissingRequiredHookError(PluginError):
    pass
