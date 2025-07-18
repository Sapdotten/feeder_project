import pytest
from src.gps import GpsController


@pytest.mark.parametrize(
    "source, coords",
    [
        (
            "$GPGGA,183404.00,5307.27299,N,04959.99312,E,1,10,0.92,1001.7,M,-6.4,M,,*73",
            ("5307.27299", "04959.99312")
        ),
        (
            "$GPGGA,183404.00,5307.27299,S,04959.99312,W,1,10,0.92,1001.7,M,-6.4,M,,*73",
            ("-5307.27299", "-04959.99312")
        ),
        (
            "",
            None
        )
    ]

)
def test_coords_transform(source: str, coords: tuple[str] | None) -> None:
    assert GpsController.parse_coords(source) == coords
