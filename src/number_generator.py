"""
Generate Number Sequence
"""
import logging
from pathlib import Path
from typing import Tuple
from collections.abc import Iterable

import cv2
import numpy as np
from mnist import MNIST

DATA_PATH = Path(__file__).parent / "../resources"
IMAGES = None
LABELS = None



def _load_data(data_path: str) -> Tuple[list, list]:
    """
    Loads the MNIST data from a directory containing training images and labels.

    Args:
        data_path: Path where the mnist.zip file is extracted.
    Returns:
        tuple: A tuple containing two lists - the training images and labels.

    Notes:
        The MNIST data can be downloaded from: https://data.deepai.org/mnist.zip.
        Make sure to extract the mnist.zip file and provide the path to the extracted directory.
        This function is later used to initialize the global variable Images and Labels.
    """

    try:
        # Loading the data
        images, labels = MNIST(data_path).load_training()

        # Converting the labels to array
        labels = np.array(labels, dtype="int16")

        # class_indices: A list containing list of indices corresponding to each unique class.
        #                [[10 , 31, 34 ...] , [1, 7, 11 ...]    , [23, 54, 32 ...]  , ...]
        #                class-0 indexes      class-1 indexes     class-2 indexes
        class_indices = [np.where(labels == i)[0] for i in np.unique(labels)]
        return images, class_indices

    except Exception as err:
        logging.error("An error occurred while loading the MNIST data: %s "
                      "Make sure that the directory exists with MNIST data inside it. "
                      "Download the dataset from: https://data.deepai.org/mnist.zip", str(err))
        raise ValueError("Failed to load the MNIST data.") from err


def _get_image(images: list, idx: int) -> np.array:
    """
    Fetches an image from the global Images list, removes the
    horizontal paddings from front and back, and inverts the
    pixel values (like: 255.0 -> 0.0 and 0.0 -> 255.0).

    Args:
        images: List containing all the images from MNIST data.
        idx: Index of the image to be fetched.
    Returns:
        np.array: Array of the image, without any horizontal paddings.
    """
    try:
        # Converting the image to array
        image = np.array(images[idx]).reshape(28, 28)
        # Creating a boolean array copy
        _image = image.astype(bool)

        # All the x-coordinates where the pixel value is True
        _x_cords = np.where(_image == True)[1]

        # Clipping the horizontal paddings
        #       ^ y axis
        #       |
        #       |    @@@@@@@
        #       |    @@
        #       |    @@@@@@@
        #       |          @@
        #       |    @@@@@@@
        #       ----|--------|----> x axis
        #        (x-min)  (x-max)
        image = image[:, np.min(_x_cords):np.max(_x_cords)]

        # Inverting the pixel values as we want the letters in black and background as white.
        image = 255.0 - image
        return image

    except Exception as err:
        logging.error('An error was occurred while processing image: %s', str(err))
        raise ValueError('Invalid input error or image processing error.') from err


def generate_numbers_sequence(digits: Iterable[int], spacing_range: Tuple[int, int], image_width: int) -> np.ndarray:
    """
    Generate an image that contains the sequence of given numbers, spaced randomly using a uniform distribution.

    Args:
        digits: An iterable containing the numerical values of the digits from which
                the sequence will be generated (for example [3, 5, 0]).
                Each value should be between 0 and 9. Otherwise, it raises an Exception.
        spacing_range: A (minimum, maximum) int pair (tuple), representing the min and max spacing
                       between digits. Unit is pixel.
        image_width: Specifies the width of the image in pixels.

    Returns:
        np.ndarray: The image containing the sequence of numbers. Image represented as floating
                    point 32bits numpy arrays with a scale ranging from 0 (black) to 1 (white),
                    the first dimension corresponding to the height and the second dimension to the width.
    """
    try:
        # Fetching the global variables and initializing them, if not already initialized.
        global IMAGES, LABELS
        if IMAGES is None or LABELS is None:
            IMAGES, LABELS = _load_data(DATA_PATH)

        # Iterating on all the digits
        combined_img = []
        for i in digits:
            # Check if the digit is between 0 and 9
            if 0 <= i <= 9:
                # Selecting a random image of a particular class
                image = _get_image(IMAGES, np.random.choice(LABELS[i]))
                # Creating a random white-space between the specified range
                white_space = np.ones((28, np.random.randint(low=spacing_range[0], high=spacing_range[1])))*255.0
                # Combining image and white-space with the rest of images
                combined_img += [image, white_space]
            else:
                raise ValueError('The numbers inside the sequence should be single digit numbers between 0 and 1.')

        # Concatenating all digits and white-spaces to a single image
        combined_img = np.concatenate(combined_img[:-1], axis=1, dtype="float32")
        # Adjusting to the user specified image-width
        resized_image = cv2.resize(combined_img, (image_width, 28))
        # Normalizing the pixel values between 0 (black) and 1 (white)
        normalized_image = np.round(resized_image/255.0, decimals=2)
        return normalized_image

    except Exception as err:
        logging.error("An error occurred while generating the number sequence: %s "
                      "Make sure digits argument is not empty and correct sequence of digits "
                      "are passed to the function.", str(err))
        raise ValueError('Number sequence generation failed.') from err
