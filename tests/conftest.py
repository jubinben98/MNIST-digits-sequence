import os
import shutil

import pytest
import number_generator
from number_generator import _load_data


@pytest.fixture(scope="module")
def images_labels():
    """
    Fixture for loading the images and labels.
    """
    images, labels = _load_data(number_generator.DATA_PATH)
    return images, labels

@pytest.fixture(scope="function")
def temporary_directory():
    """
    Creates and removes a temporary dictionaries.
    """
    TEMP_DIR_PATH = "./test_directory"
    # Creating the test directory
    os.mkdir(TEMP_DIR_PATH)
    yield TEMP_DIR_PATH
    # Removing the test directory - teardown/cleanup
    shutil.rmtree(TEMP_DIR_PATH)