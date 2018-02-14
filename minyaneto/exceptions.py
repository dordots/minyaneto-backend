class MinyanetoApplicationError(Exception):
    pass


class MissingConfigurationError(MinyanetoApplicationError):
    pass


class ValidationError(MinyanetoApplicationError):
    pass


class HttpRequestError(MinyanetoApplicationError):
    pass


class TestError(MinyanetoApplicationError):
    pass


class DataIntegrityError(MinyanetoApplicationError):
    pass
