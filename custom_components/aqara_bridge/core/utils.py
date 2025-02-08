"""the Aqara Bridge utils."""

from datetime import datetime

from homeassistant.core import HomeAssistant
from homeassistant.util.dt import DEFAULT_TIME_ZONE, get_time_zone


def local_zone(hass=None):
    try:
        if isinstance(hass, HomeAssistant):
            return get_time_zone(hass.config.time_zone)
        return DEFAULT_TIME_ZONE
    except KeyError:
        pass
    return DEFAULT_TIME_ZONE


def ts_format_str_ms(str_timestamp_ms: str, hass=None):
    if str_timestamp_ms:
        timestamp = round(int(str_timestamp_ms) / 1000, 0)
        return datetime.fromtimestamp(timestamp, local_zone(hass))


def ts_format_str_s(str_timestamp_s: str, hass=None):
    if str_timestamp_s:
        timestamp = int(str_timestamp_s)
        return datetime.fromtimestamp(timestamp, local_zone(hass))


def light_convert_unit32_to_xy(value: int) -> tuple[float, float]:
    x_int = (value >> 16) & 0xFFFF
    y_int = value & 0xFFFF
    x = x_int / 65535.0
    y = y_int / 65535.0
    return (x, y)


def light_convert_xy_to_uint32(x: float, y: float) -> int:
    x_int = int(round(x * 65535)) & 0xFFFF
    y_int = int(round(y * 65535)) & 0xFFFF
    return (x_int << 16) | y_int


def light_convert_argb_to_rgb(argb: int) -> tuple[int, int, int]:
    r = (argb >> 16) & 0xFF
    g = (argb >> 8) & 0xFF
    b = argb & 0xFF
    return (r, g, b)


def light_convert_rgb_to_argb(rgb: tuple[int, int, int], a: int = 255) -> int:
    r, g, b = rgb
    return ((a & 0xFF) << 24) | ((r & 0xFF) << 16) | ((g & 0xFF) << 8) | (b & 0xFF)
