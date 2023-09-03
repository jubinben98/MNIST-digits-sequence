import numpy as np
import pytest
import number_generator
from number_generator import _load_data, _get_image, generate_numbers_sequence


# Test cases for _load_data
def test_case_1(images_labels):
    """
    Check if the _load_data function loads the images and labels correctly.
    """
    images = images_labels[0]
    labels = images_labels[1]
    assert all((len(images) == 60000, len(labels) == 10))

def test_case_2():
    """
    Check if _load_data raises a ValueError for an invalid path.
    """
    with pytest.raises(ValueError):
        _ = _load_data('../MNIST_DATA_PATH')

# Test cases for _get_image
def test_case_3(images_labels):
    """
    Check if _get_image returns the correct image with a valid index.
    """
    image = _get_image(images_labels[0], 0)
    image = image.astype(bool)
    _x_cords = np.where(image == True)[1]
    assert all((0 in _x_cords, image.shape[1]-1 in _x_cords))

def test_case_4(images_labels):
    """
    Check if _get_image raises a ValueError for an invalid index.
    """
    with pytest.raises(ValueError):
        _ = _get_image(images_labels[1], 0)

# Test cases for generate_numbers_sequence
def test_case_5(images_labels):
    """
    Check the dtype of the generated image.
    """
    number_generator.IMAGES = images_labels[0]
    number_generator.LABELS = images_labels[1]
    image = generate_numbers_sequence(digits=[1, 2, 3],
                                      spacing_range=(2, 5),
                                      image_width=50)
    assert image.dtype == np.float32

def test_case_6(images_labels):
    """
    Check the shape of the generated image.
    """
    number_generator.IMAGES = images_labels[0]
    number_generator.LABELS = images_labels[1]

    width = 50
    image = generate_numbers_sequence(digits=[1, 2, 3],
                                      spacing_range=(2, 5),
                                      image_width=width)
    assert image.shape == (28, width)

def test_case_7(images_labels):
    """
    Check the range of the generated image.
    """
    number_generator.IMAGES = images_labels[0]
    number_generator.LABELS = images_labels[1]

    width = 50
    image = generate_numbers_sequence(digits=[1, 2, 3],
                                      spacing_range=(2, 5),
                                      image_width=width)
    assert all((np.min(image) >= 0.0, np.max(image) <= 1.0))

def test_case_8(images_labels):
    """
    Check if it raises a ValueError for an invalid input.
    """
    with pytest.raises(ValueError):
        number_generator.IMAGES = images_labels[0]
        number_generator.LABELS = images_labels[1]

        generate_numbers_sequence(digits=[],
                                  spacing_range=(2, 5),
                                  image_width=50)

def test_case_9(images_labels):
    """
    Check if it raises a ValueError for an invalid input.
    """
    with pytest.raises(ValueError):
        number_generator.IMAGES = images_labels[0]
        number_generator.LABELS = images_labels[1]

        generate_numbers_sequence(digits=[1, 1, 12],
                                  spacing_range=(2, 5),
                                  image_width=50)

def test_case_10(images_labels):
    """
    Check if it raises a ValueError for an invalid input.
    """
    with pytest.raises(ValueError):
        number_generator.IMAGES = images_labels[0]
        number_generator.LABELS = images_labels[1]

        generate_numbers_sequence(digits=[1, 2],
                                  spacing_range=(),
                                  image_width=50)

def test_case_11(images_labels):
    """
    Check if it raises a ValueError for an invalid input.
    """
    with pytest.raises(ValueError):
        number_generator.IMAGES = images_labels[0]
        number_generator.LABELS = images_labels[1]

        generate_numbers_sequence(digits=[1, 2],
                                  spacing_range=(2, 5),
                                  image_width=None)