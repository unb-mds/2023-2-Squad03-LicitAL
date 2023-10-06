from enum import Enum


class Timeouts(Enum):
    READ_TIMEOUT = 60
    CONNECT_TIMEOUT = 60
    NUM_REQUEST_RETRIES = 3