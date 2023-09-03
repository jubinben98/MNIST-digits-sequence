"""
Script for generating handwritten number sequence images using CLI
"""

import logging
import os
import random
from typing import Tuple

import click
import cv2
import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm
from number_generator import generate_numbers_sequence

logging.basicConfig(level=logging.DEBUG)


def generate_area_code(phone_num_type: int, mobile_code: list) -> list:
    """
    Generates a sequence of area code according the phone number type

    Args:
        phone_num_type:
        mobile_code:
    Returns:
        list: A list of sequence with 2-6 digits, starting with 0.
    """
    try:
        _area_code = []
        # If phone_num_type > 5, then select a mobile code as area code
        if phone_num_type > 5:
            _area_code = random.choice(mobile_code)
        # If phone_num_type < 5, then create <phone_num_type> digit random sequence starting with 0
        else:
            _area_code += [0, *np.random.choice([*range(1, 10)], size=phone_num_type).tolist()]
        return _area_code

    except Exception as error:
        logging.error("Error occurred generating the area code of phone number: %s", str(error))
        raise ValueError("Area code of phone number generation failed.") from error

def generate_exchange_number(exchange_number_size: int, is_mobile_number: bool) -> list:
    """
    Generates a sequence of exchange number according to size of area code type

    Args:
        exchange_number_size: Size of the exchange number.
        is_mobile_number: Sequence is being generated for a mobile number or not.
    Returns:
        list: A list of sequence with 0-4 digits, depending upon the area code.
    """
    try:
        # If the area code is a mobile-phone-code then exchange_number_size should be 4
        exchange_number_size = (exchange_number_size, 4)[is_mobile_number]
        exchange_number = (np.random.choice([*range(0, 10)], size=exchange_number_size)).tolist()
        return exchange_number

    except Exception as error:
        logging.error('Error occurred generating the exchange-number of phone number: %s', str(error))
        raise ValueError("Exchange-number of phone number generation failed.") from error

def generate_subscriber_number() -> list:
    """
    Generates a sequence of 4 digit random subscriber number.

    Returns:
        list: A list of sequence with random 4 digits.
    """
    try:
        subscriber_number = (np.random.choice([*range(0, 10)], size=4)).tolist()
        return subscriber_number

    except Exception as error:
        logging.error('Error occurred generating the subscriber-number of phone number: %s', str(error))
        raise ValueError("Subscriber-number of phone number generation failed.") from error

def add_noise(image: np.ndarray, stddev_range: Tuple[int, int]=(0, 255)) -> np.ndarray:
    """
    Add Gaussian noise to an input image.

    Args:
        image: A normalized input image to which noise will be added.
        stddev_range: Defines the range of standard-deviation from which random value should be picked.
    Returns:
        np.ndarray: A noisy image array, with the same shape as the input image.
    """
    try:
        # Generate a random standard deviation for the Gaussian noise in the range [1, 200]
        stddev = np.random.randint(stddev_range[0], stddev_range[1])
        # Create a noise array with the same shape as the input image
        noise = np.zeros(image.shape, np.float32)
        # The mean is set to 255 so that the noise could be centered around a bright value
        cv2.randn(noise, 255, stddev)
        # Apply the normalized noise array to the original image, effectively adding the noise
        noisy_img = cv2.bitwise_and(image, noise/255.0)
        return noisy_img
    except Exception as error:
        logging.error('Error occurred adding the noise to the phone number image: %s', str(error))
        raise ValueError("Noise adding operation failed.") from error

def combine_phone_number(area_code: list, exchange_number: list, subscriber_number: list,
                         writing_style_type: int, spacing_range:Tuple[int, int], img_width: int) -> np.ndarray:
    """
    Fetches all the 3 parts of a phone number and generates an image for each part individually.
    And combines them based of the writing style type.

    Args:
        area_code: 2-3 digits and usually starts with 0.
        exchange_number: 2-4 digits, depending upon the area code
        subscriber_number: 2-3 digits and usually starts with 0.
        writing_style_type: Style-1 or Style-2
        spacing_range: A (minimum, maximum) int pair (tuple), representing the min and max spacing
                       between digits. Unit is pixel.
        img_width: Specifies the width of the image in pixels.
    Returns:
        np.ndarray: An image of phone number represented in float32 bits array, with user definer
                    width, user defined consecutive spaces and random part spaces (for style-2) if applicable.
    """
    try:
        _image = None
        # Part space to be used for style-2.
        #   Eg: 070 <min_part_space> 1234 <min_part_space> 5678
        min_part_space = 25
        combined_image = []

        # Writing Style-1 Eg: 07012345678, 0211234567
        if writing_style_type == 1:
            sequence = area_code + exchange_number + subscriber_number
            _image = generate_numbers_sequence(digits=sequence, spacing_range=spacing_range, image_width=img_width)
            # Adding some white-space in the front and back
            white_space = np.ones((28, np.random.randint(low=spacing_range[0], high=spacing_range[1]) + 5))
            combined_image = [white_space, _image, white_space]

        # Writing Style-2 Eg: 070 1234 5678, 021 123 4567
        elif writing_style_type == 2:
            # Generating the image of area code
            area_code_image = generate_numbers_sequence(digits=area_code, spacing_range=spacing_range,
                                                        image_width=28*len(area_code))
            # Generating the image for part space
            part_space = np.ones((28, np.random.randint(low=spacing_range[0], high=spacing_range[1]) + min_part_space))
            combined_image += [area_code_image, part_space]

            if exchange_number:
                # Generating the image of exchange number
                exchange_number_image = generate_numbers_sequence(digits=exchange_number, spacing_range=spacing_range,
                                                                  image_width=28*len(exchange_number))
                # Generating the image for part space
                part_space = np.ones((28, np.random.randint(low=spacing_range[0], high=spacing_range[1])+min_part_space))
                combined_image += [exchange_number_image, part_space]

            # Generating the image of a subscriber number
            subscriber_number_image = generate_numbers_sequence(digits=subscriber_number, spacing_range=spacing_range,
                                                                image_width=28*len(subscriber_number))
            combined_image += [subscriber_number_image]

            # Adding some white-space in the front and back
            white_space = np.ones((28, np.random.randint(low=spacing_range[0], high=spacing_range[1]) + 5))
            combined_image = [white_space]+combined_image+[white_space]

        # Combining all the images
        _image = np.concatenate(combined_image, axis=1, dtype='float32')
        # Resizing to the user defined image width
        _image = cv2.resize(_image, (img_width, 28))
        return _image

    except Exception as error:
        logging.error("Error occurred during final number generation: %s", str(error))
        raise ValueError("Final number generation failed.") from error

def generate_phone_number(spacing_range: Tuple[int, int], image_width: int, output_path: str, num_images: int) -> None:
    """
    Main function call for generating random Japanese phone numbers
    The phone numbers are generated in 3 parts and images are saved
    in 2 different types of writing styles. For more details read
    the Notes section from above.

    Args:
        spacing_range: A (minimum, maximum) int pair (tuple), representing the min and max spacing
                       between digits. Unit is pixel.
        image_width: Specifies the width of the image in pixels.
        output_path: Specifies the path where the generated image should be stored.
        num_images: Number of images to be generated
    Returns:
        None: Saves N number of random Japanese phone number images at a given directory.
    """

    try:
        # Randomly selecting the type of phone numbers to be generated
        phone_number_type = np.random.choice([*range(1, 10)], size=num_images)
        # Randomly selecting the writing style to be used for each phone number
        style_type  = np.random.choice([1, 2], size=num_images)
        # Predefining the mobile number code
        mobile_code = [[0, 7, 0], [0, 8, 0], [0, 9, 0]]

        # Generating N number of random phone numbers iteratively
        for i in tqdm(range(num_images)):
            # Generating the area code - part(1/3)
            area_code = generate_area_code(phone_number_type[i], mobile_code)

            # Generating the exchange number - part(2/3)
            is_mobile_number = area_code in mobile_code
            # Calculating the Exchange number size based on the area code
            exchange_number_size = 6-len(area_code)
            exchange_number = generate_exchange_number(exchange_number_size, is_mobile_number)

            # Generating the subscriber number - part(3/3)
            subscriber_number = generate_subscriber_number()

            # Generating an image by combining all 3-parts of the phone number
            _image  = combine_phone_number(area_code, exchange_number, subscriber_number, style_type[i], spacing_range, image_width)

            # Adding random noise to the generated image
            _image = add_noise(_image)

            # Saving the image with phone-number as filename
            file_name = f"{''.join(map(str, area_code + exchange_number + subscriber_number))}.png"
            plt.imsave(os.path.join(output_path, file_name), _image, cmap='gray')

    except Exception as error:
        logging.error("Error occurred in the main: %s", str(error))
        raise ValueError("Number generation failed.") from error

@click.group()
def main():
    """
    Number Generator CLI
    This command-line interface (CLI) serves as the entry point for using the Number Generator package.
    It provides several subcommands for generating image-sequences of numbers and random phone number images.

    To use the Number Generator CLI, run one of the following subcommands:
    - To generate an image from an input sequence of digits, use:
      $ python number-generator-script.py generate-numbers-sequence --sequence 123 --min-space 2 --max-space 4 --image-width 60

    - To generate random phone number images, use:
      $ python number-generator-script.py generate-phone-numbers --min-space 2 --max-space 4 --image-width 60 --num-images 5

    For detailed information on each subcommand and their options, run:
      $ python number-generator-script.py.py [subcommand] --help

    Subcommands:
    ------------
    - generate-numbers-sequence: Generates an image from an input sequence of digits.
    - generate-phone-numbers: Generates random phone number images.
    """
    pass

#--------------------------------------------------------------------------------------------#
#   CLI - 1: A low-level CLI for the above API that uses the generate_numbers_sequence API   #
#--------------------------------------------------------------------------------------------#
@main.command("generate-numbers-sequence", help="Generates an image from input sequence")
@click.option('--sequence', type=int, required=True, help="The sequence of digits to be generated")
@click.option('--min-space', type=int, required=True, help="Min-space between consecutive digits")
@click.option('--max-space', type=int, required=True, help="Max-space between consecutive digits")
@click.option('--image-width', type=int, required=True, help="Width of the generated image")
@click.option('--output-path', help="Path where the generated image should be stored", default=".")
def main_generate_numbers_sequence(sequence: int, min_space: int, max_space: int, image_width: int, output_path: str):
    """
    Generates an image from the input sequence of digits.

    Args
        sequence: The sequence of digits to be generated as an image.
        min_space: Minimum space (in pixels) between consecutive digits in the generated image.
        max_space: Maximum space (in pixels) between consecutive digits in the generated image.
        image_width: Width of the generated image in pixels.
        output_path: Path where the generated image should be stored. Default is the current directory.
    Returns:
        None, saves the generated images at the specified location.
    """
    try:
        logging.info("Generating the number sequence")
        # Converting sequence to list of digits
        sequence = list(map(int, str(sequence)))

        # Function call for generating the number sequence
        image = generate_numbers_sequence(digits=sequence, spacing_range=(min_space, max_space), image_width=image_width)
        logging.info("Image generated")

        # Defining the sequence as the file-name. Eg: 123.png, 9876.png, etc.
        filename = f"{''.join(map(str, sequence))}.png"
        # Saving the png image to the output path
        plt.imsave(os.path.join(output_path, filename), image, cmap='gray')
        logging.info("Saved image path: %s", os.path.join(output_path, filename))

    except ValueError as err:
        logging.error("Error occurred generating the number sequence: %s Provide valid arguments to the script."
                      " For more details, checkout the ReadMe usage guide.", str(err))
        raise ValueError("Number sequence generation failed.") from err


# ----------------------------------------------------------------------------------------------#
#   CLI - 2: A CLI to generate an image dataset of random sequences of Japanese phone numbers   #
# ----------------------------------------------------------------------------------------------#
@main.command("generate-phone-numbers", help="Generates random phone number images")
@click.option('--min-space', type=int, required=True,  help="Min-space between the digits")
@click.option('--max-space', type=int, required=True,  help="Max-space between the digits")
@click.option('--image-width', type=int, required=True,  help="Width of the generated image")
@click.option('--num-images', type=int, required=True,  help="Number of images to generate")
@click.option('--output-path', required=True,  help="Path for generated image", default=".")
def main_generate_phone_numbers(min_space: int, max_space: int, image_width: int, output_path: str, num_images: int):
    """
    This function is a CLI command that generates a specified number of random phone number images
    with the given spacing and image width. The images are saved in the specified output_path.

    Args
        min_space : Minimum space (in pixels) between the digits in the generated images.
        max_space : Maximum space (in pixels) between the digits in the generated images.
        image_width : Width of the generated images in pixels.
        output_path : Path where the generated images will be saved. Default is the current directory.
        num_images : Number of images to generate.
    Returns:
        None, saves the generated images at the specified location.
    Notes:
         Please refer to the ProjectReadMe.md inside MNIST-digits-sequence/docs for some context
         behind the execution.
    """
    try:
        if num_images > 0:
            # Calling the main function to generate phone numer
            logging.info("Generating %d random phone numbers", num_images)
            generate_phone_number((min_space, max_space), image_width, output_path, num_images)

            logging.info("Generated images saved at: %s", output_path)
        else:
            raise ValueError("The num_images arguments should be greater 0.")

    except ValueError as err:
        logging.error("Error occurred generating the number sequence: %s Provide valid arguments to the script."
                      " For more details, checkout the ReadMe usage guide.", str(err))
        raise ValueError("Number sequence generation failed.") from err

if __name__ == "__main__":
    main()
