import os


class Config(object):
    DEBUG = False
    SQLALCHEMY_ECHO = False

    # Application threads. A common general assumption is
    # using 2 per available processor cores - to handle
    # incoming requests using one and performing background
    # operations using the other.
    THREADS_PER_PAGE = 2

    # Enable protection against *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = True

    # Use a secure, unique and absolutely secret key for
    # signing the data.
    CSRF_SESSION_KEY = "secret-ssk09lJUa3@shushuststy@WRTDGCYTppkmiGGi"

    # Secret key for signing cookies
    SECRET_KEY = "agyg87ssk09lJUa3@sedyuy+RijoijaUHT21wsAvzbmx.momiJHBJJSYY00Lo"

    SQLALCHEMY_POOL_SIZE = 5
    ELASTIC_SEARCH_HOSTS = ['https://search-startach-es-kjunyv6dur2zgmoygirwebhxaa.us-east-1.es.amazonaws.com']
