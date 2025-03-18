import decimal
import logging
import uuid
from datetime import date, datetime, time, timedelta
from typing import Any, Callable, Optional, Union

import numpy as np
import pandas as pd
import simplejson
from simplejson import JSONDecodeError


logger = logging.getLogger(__name__)


def format_timedelta(time_delta: timedelta) -> str:
    """
    Ensures negative time deltas are easily interpreted by humans

    >>> td = timedelta(0) - timedelta(days=1, hours=5,minutes=6)
    >>> str(td)
    '-2 days, 18:54:00'
    >>> format_timedelta(td)
    '-1 day, 5:06:00'
    """
    if time_delta < timedelta(0):
        return "-" + str(abs(time_delta))

    # Change this to format positive time deltas the way you want
    return str(time_delta)


def base_json_conv(obj: Any) -> Any:
    """
    Tries to convert additional types to JSON compatible forms.

    :param obj: The serializable object
    :returns: The JSON compatible form
    :raises TypeError: If the object cannot be serialized
    :see: https://docs.python.org/3/library/json.html#encoders-and-decoders
    """

    if isinstance(obj, memoryview):
        obj = obj.tobytes()
    if isinstance(obj, np.int64):
        return int(obj)
    if isinstance(obj, np.bool_):
        return bool(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, set):
        return list(obj)
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    if isinstance(obj, (uuid.UUID, time)):
        return str(obj)
    if isinstance(obj, timedelta):
        return format_timedelta(obj)
    if isinstance(obj, bytes):
        try:
            return obj.decode("utf-8")
        except Exception:  # pylint: disable=broad-except
            try:
                return obj.decode("utf-16")
            except Exception:  # pylint: disable=broad-except
                return "[bytes]"

    raise TypeError(f"Unserializable object {obj} of type {type(obj)}")


def json_iso_dttm_ser(obj: Any, pessimistic: bool = False) -> Any:
    """
    A JSON serializer that deals with dates by serializing them to ISO 8601.

        >>> json.dumps({'dttm': datetime(1970, 1, 1)}, default=json_iso_dttm_ser)
        '{"dttm": "1970-01-01T00:00:00"}'

    :param obj: The serializable object
    :param pessimistic: Whether to be pessimistic regarding serialization
    :returns: The JSON compatible form
    :raises TypeError: If the non-pessimistic object cannot be serialized
    """

    if isinstance(obj, (datetime, date, pd.Timestamp)):
        return obj.isoformat()

    try:
        return base_json_conv(obj)
    except TypeError:
        if pessimistic:
            logger.error("Failed to serialize %s", obj)
            return f"Unserializable [{type(obj)}]"
        raise


def pessimistic_json_iso_dttm_ser(obj: Any) -> Any:
    """Proxy to call json_iso_dttm_ser in a pessimistic way

    If one of object is not serializable to json, it will still succeed"""
    return json_iso_dttm_ser(obj, pessimistic=True)


def validate_json(obj: Union[bytes, bytearray, str]) -> None:
    """
    A JSON Validator that validates an object of bytes, bytes array or string
    to be in valid JSON format

    :raises SupersetException: if obj is not serializable to JSON
    :param obj: an object that should be parseable to JSON
    """
    if obj:
        try:
            loads(obj)
        except JSONDecodeError as ex:
            logger.error("JSON is not valid %s", str(ex), exc_info=True)
            raise


def dumps(  # pylint: disable=too-many-arguments
    obj: Any,
    default: Optional[Callable[[Any], Any]] = None,
    allow_nan: bool = False,
    ignore_nan: bool = True,
    sort_keys: bool = False,
    indent: Union[str, int, None] = None,
    separators: Union[tuple[str, str], None] = None,
    cls: Union[type[simplejson.JSONEncoder], None] = None,
) -> str:
    """
    Dumps object to compatible JSON format

    :param obj: The serializable object
    :param default: function that should return a serializable version of obj
    :param allow_nan: when set to True NaN values will be serialized
    :param ignore_nan: when set to True nan values will be ignored
    :param sort_keys: when set to True keys will be sorted
    :param indent: when set elements and object members will be pretty-printed
    :param separators: when specified dumps will use (item_separator, key_separator)
    :param cls: custom `JSONEncoder` subclass
    :returns: String object in the JSON compatible form
    """

    results_string = ""
    try:
        results_string = simplejson.dumps(
            obj,
            default=default,
            allow_nan=allow_nan,
            ignore_nan=ignore_nan,
            sort_keys=sort_keys,
            indent=indent,
            separators=separators,
            cls=cls,
        )
    except UnicodeDecodeError:
        results_string = simplejson.dumps(
            obj,
            default=default,
            allow_nan=allow_nan,
            ignore_nan=ignore_nan,
            sort_keys=sort_keys,
            indent=indent,
            separators=separators,
            cls=cls,
            encoding=None,
        )
    return results_string


def loads(
    obj: Union[bytes, bytearray, str],
    encoding: Union[str, None] = None,
    allow_nan: bool = False,
    object_hook: Union[Callable[[dict[Any, Any]], Any], None] = None,
) -> Any:
    """
    deserializable instance to a Python object.

    :param obj: The deserializable object
    :param encoding: determines the encoding used to interpret the obj
    :param allow_nan: if True it will allow the parser to accept nan values
    :param object_hook: function that will be called to decode objects values
    :returns: A Python object deserialized from string
    """
    return simplejson.loads(
        obj,
        encoding=encoding,
        allow_nan=allow_nan,
        object_hook=object_hook,
    )

