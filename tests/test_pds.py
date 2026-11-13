import numpy as np
import pytest

from analog.pds import parse_label, read_image

LABEL = """PDS_VERSION_ID = PDS3
PRODUCT_ID = "TINY"
OBJECT = IMAGE
  LINES = 2
  LINE_SAMPLES = 4
  SAMPLE_TYPE = MSB_INTEGER
  SAMPLE_BITS = 16
END_OBJECT = IMAGE
OBJECT = IMAGE_MAP_PROJECTION
  MAP_PROJECTION_TYPE = "SIMPLE CYLINDRICAL"
  A_AXIS_RADIUS = 3396.0 <KM>
  POSITIVE_LONGITUDE_DIRECTION = "EAST"
  MAP_RESOLUTION = {resolution} <PIXEL/DEGREE>
  MAXIMUM_LATITUDE = 90.0 <DEGREE>
  WESTERNMOST_LONGITUDE = {west} <DEGREE>
END_OBJECT = IMAGE_MAP_PROJECTION
END
"""


def write_product(tmp_path, west):
    values = np.array([[1, 2, 3, 4], [5, 6, 7, 8]], dtype=">i2")
    image = tmp_path / "tiny.img"
    values.tofile(image)
    resolution = 4 / 360  # 4 samples around the globe
    image.with_suffix(".lbl").write_text(LABEL.format(resolution=resolution, west=west))
    return image


def test_parse_label_strips_quotes_and_units(tmp_path):
    label = parse_label(write_product(tmp_path, west=-180.0).with_suffix(".lbl"))
    assert label["MAP_PROJECTION_TYPE"] == "SIMPLE CYLINDRICAL"
    assert label["A_AXIS_RADIUS"] == "3396.0"
    assert label["LINES"] == "2"


def test_read_image_coordinates(tmp_path):
    image = read_image(write_product(tmp_path, west=-180.0))
    assert image.dims == ("lat", "lon")
    np.testing.assert_allclose(image.lat, [45, -45])
    np.testing.assert_allclose(image.lon, [-135, -45, 45, 135])
    np.testing.assert_array_equal(image.values, [[1, 2, 3, 4], [5, 6, 7, 8]])


def test_read_image_moves_0_360_longitudes_to_180_180(tmp_path):
    image = read_image(write_product(tmp_path, west=0.0))
    np.testing.assert_allclose(image.lon, [-135, -45, 45, 135])
    # Source columns sat at 45, 135, 225 (-135) and 315 (-45) east.
    np.testing.assert_array_equal(image.values, [[3, 4, 1, 2], [7, 8, 5, 6]])


def test_read_image_rejects_wrong_file_size(tmp_path):
    image = write_product(tmp_path, west=-180.0)
    image.write_bytes(image.read_bytes()[:-2])
    with pytest.raises(ValueError, match="size"):
        read_image(image)
