"""Unambiguous JSON ingestion for offline review artifacts."""
import json
import math


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON member: {key}")
        result[key] = value
    return result


def _finite_float(value):
    number = float(value)
    if not math.isfinite(number):
        raise ValueError("JSON numbers must be finite")
    return number


def _reject_constant(value):
    raise ValueError(f"Nonstandard JSON constant: {value}")


def parse_json(data):
    """Parse the same bytes used for a provenance hash."""
    return json.loads(data, object_pairs_hook=_unique_object,
                      parse_constant=_reject_constant, parse_float=_finite_float)


def load_json(path):
    """Reject duplicate keys and nonfinite numbers at every nesting level."""
    return parse_json(path.read_bytes())
