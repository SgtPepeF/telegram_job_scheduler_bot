from .constants import (
    DIRECTIONS,
    BASE_OPEN_WEATHER_API_URL,
)
from settings import (
    OPEN_WEATHER_API_TOKEN,
    DEFAULT_OPENWEATHER_REGION
)


def get_openweather_url(city=DEFAULT_OPENWEATHER_REGION, lon=None, lat=None):
    url = f'{BASE_OPEN_WEATHER_API_URL}?appid={OPEN_WEATHER_API_TOKEN}&lang=ru&units=metric'
    if city:
        return f'{url}&q={city}'
    elif lon and lat:
        return f'{url}&lat={lat}&lon={lon}'

    raise LookupError(
        'url must contain either city name or lon and lat of location.'
    )


def compass_direction(direction_deg: float) -> str:
    """Evaluates direction by azimuth degree."""

    # Центрирование компаса + защита от дурака.
    deg = (direction_deg + 22.5) % 360
    direction_index = int(deg // 45)
    return DIRECTIONS[direction_index]
