DIRECTIONS = ('N', 'N-E', 'E', 'S-E', 'S', 'S-W', 'W', 'N-W')


def compass_direction(direction_deg: float) -> str:
    """Evaluates direction by degree."""

    # Центрирование компаса + защита от дурака.
    deg = (direction_deg + 22.5) % 360
    direction_index = int(deg // 45)
    return DIRECTIONS[direction_index]
