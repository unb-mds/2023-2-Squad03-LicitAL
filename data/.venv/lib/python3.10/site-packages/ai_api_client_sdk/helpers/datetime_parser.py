from datetime import datetime


DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
DATETIME_FORMAT_FLOAT = '%Y-%m-%dT%H:%M:%S.%fZ'
DATETIME_FORMAT_36 = "%Y-%m-%dT%H:%M:%S+00:00"
DATETIME_FORMAT_FLOAT_TZ = '%Y-%m-%dT%H:%M:%S.%f+00:00'


def parse_datetime(datetime_str: str) -> datetime:
    try:
        return datetime.strptime(datetime_str, DATETIME_FORMAT_36)
    except ValueError as _:
        try:
            return datetime.strptime(datetime_str, DATETIME_FORMAT)
        except ValueError as _:
            try:
                return datetime.strptime(datetime_str, DATETIME_FORMAT_FLOAT)
            except ValueError as _:
                if len(datetime_str) > 32:
                    datetime_str = f'{datetime_str[:26]}{datetime_str[29:]}'
                return datetime.strptime(datetime_str, DATETIME_FORMAT_FLOAT_TZ)
