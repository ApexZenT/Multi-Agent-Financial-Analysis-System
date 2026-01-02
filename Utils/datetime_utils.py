from dateutil import parser
from datetime import datetime, timezone
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# Map common timezone abbreviations to UTC offsets (seconds)
TZINFOS = {
    "ET": -5 * 3600,
    "EST": -5 * 3600,
    "EDT": -4 * 3600,
    "CT": -6 * 3600,
    "CST": -6 * 3600,
    "CDT": -5 * 3600,
    "MT": -7 * 3600,
    "MST": -7 * 3600,
    "MDT": -6 * 3600,
    "PT": -8 * 3600,
    "PST": -8 * 3600,
    "PDT": -7 * 3600,
}


def parse_datetime(
    dt_str: Optional[str], default_tz: timezone = timezone.utc
) -> Optional[datetime]:
    """
    Parse a datetime string into a Python datetime object.

    Args:
        dt_str: The string to parse.
        default_tz: Timezone to assign if the string is naive.

    Returns:
        datetime object (aware) or None if input is None or invalid.
    """
    if not dt_str:
        return None

    try:
        dt = parser.parse(dt_str, tzinfos=TZINFOS)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=default_tz)
        # Normalize to UTC
        dt = dt.astimezone(timezone.utc)
        return dt
    except (ValueError, TypeError) as e:
        logger.warning("Could not parse datetime '%s': %s", dt_str, e)
        return None
