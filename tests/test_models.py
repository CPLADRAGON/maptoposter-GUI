import pytest

from maptoposter_core.models import PosterRequest


def test_poster_request_defaults_are_cli_defaults():
    request = PosterRequest(city="Paris", country="France")

    assert request.theme == "terracotta"
    assert request.distance == 18000
    assert request.width == 12.0
    assert request.height == 16.0
    assert request.output_format == "png"


def test_requires_city_and_country():
    with pytest.raises(ValueError, match="City is required"):
        PosterRequest(city="", country="France").validate()

    with pytest.raises(ValueError, match="Country is required"):
        PosterRequest(city="Paris", country="").validate()


def test_coordinates_must_be_paired():
    with pytest.raises(ValueError, match="provided together"):
        PosterRequest(city="Paris", country="France", latitude="48.85").validate()


def test_dimensions_are_limited_to_twenty_inches():
    with pytest.raises(ValueError, match="20 inches or less"):
        PosterRequest(city="Paris", country="France", width=21).validate()


def test_supported_output_formats_only():
    with pytest.raises(ValueError, match="Output format"):
        PosterRequest(city="Paris", country="France", output_format="jpg").validate()
