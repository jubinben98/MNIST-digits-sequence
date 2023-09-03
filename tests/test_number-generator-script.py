import os.path
import subprocess
from glob import glob


def test_case_1(temporary_directory):
    """
    Checks the execution of CLI-1.
    """
    sequence = 123
    min_space = 2
    max_space = 4
    image_width = 100
    output_path = temporary_directory

    execution = subprocess.run([
        "python", "-m", "number-generator-script",
        "generate-numbers-sequence",
        "--sequence", f"{sequence}",
        "--min-space", f"{min_space}",
        "--max-space", f"{max_space}",
        "--image-width", f"{image_width}",
        "--output-path", f"{output_path}"
    ])

    output_file = os.path.basename(glob(temporary_directory+'/*.png')[0])
    assert all((execution.returncode == 0, output_file == f"{str(sequence)}.png"))

def test_case_2(temporary_directory):
    """
    Checks the CLI-1 fails with invalid input.
    """
    sequence = -123
    min_space = 2
    max_space = 4
    image_width = 100
    output_path = temporary_directory

    execution = subprocess.run([
        "python", "-m", "number-generator-script",
        "generate-numbers-sequence",
        "--sequence", f"{sequence}",
        "--min-space", f"{min_space}",
        "--max-space", f"{max_space}",
        "--image-width", f"{image_width}",
        "--output-path", f"{output_path}"
    ])
    assert execution.returncode != 0

def test_case_3(temporary_directory):
    """
    Checks the CLI-1 fails with invalid input.
    """
    sequence = 9760
    min_space = 'abc'
    max_space = 4
    image_width = 100
    output_path = temporary_directory

    execution = subprocess.run([
        "python", "-m", "number-generator-script",
        "generate-numbers-sequence",
        "--sequence", f"{sequence}",
        "--min-space", f"{min_space}",
        "--max-space", f"{max_space}",
        "--image-width", f"{image_width}",
        "--output-path", f"{output_path}"
    ])
    assert execution.returncode != 0

def test_case_4(temporary_directory):
    """
    Checks the CLI-1 fails with invalid input.
    """
    sequence = 9760
    min_space = 2
    max_space = None
    image_width = 100
    output_path = temporary_directory

    execution = subprocess.run([
        "python", "-m", "number-generator-script",
        "generate-numbers-sequence",
        "--sequence", f"{sequence}",
        "--min-space", f"{min_space}",
        "--max-space", f"{max_space}",
        "--image-width", f"{image_width}",
        "--output-path", f"{output_path}"
    ])
    assert execution.returncode != 0

def test_case_5(temporary_directory):
    """
    Checks the CLI-1 fails with invalid input.
    """
    sequence = 9760
    min_space = 2
    max_space = 4
    image_width = 'abc'
    output_path = temporary_directory

    execution = subprocess.run([
        "python", "-m", "number-generator-script",
        "generate-numbers-sequence",
        "--sequence", f"{sequence}",
        "--min-space", f"{min_space}",
        "--max-space", f"{max_space}",
        "--image-width", f"{image_width}",
        "--output-path", f"{output_path}"
    ])
    assert execution.returncode != 0

def test_case_6(temporary_directory):
    """
    Checks the execution of CLI-2.
    """
    min_space = 2
    max_space = 4
    image_width = 100
    num_images = 10
    output_path = temporary_directory

    execution = subprocess.run([
        "python", "-m", "number-generator-script",
        "generate-phone-numbers",
        "--min-space", f"{min_space}",
        "--max-space", f"{max_space}",
        "--image-width", f"{image_width}",
        "--output-path", f"{output_path}",
        "--num-images", f"{num_images}"
    ])

    output_files = glob(temporary_directory+'/*.png')
    assert all((execution.returncode == 0, len(output_files) == num_images))

def test_case_7(temporary_directory):
    """
    Checks the CLI-2 fails with invalid input.
    """
    min_space = 2
    max_space = "three"
    image_width = 100
    num_images = 10
    output_path = temporary_directory

    execution = subprocess.run([
        "python", "-m", "number-generator-script",
        "generate-phone-numbers",
        "--min-space", f"{min_space}",
        "--max-space", f"{max_space}",
        "--image-width", f"{image_width}",
        "--output-path", f"{output_path}",
        "--num-images", f"{num_images}"
    ])

    assert (execution.returncode != 0)

def test_case_8(temporary_directory):
    """
    Checks the CLI-2 fails with invalid input.
    """
    min_space = 2
    max_space = 4
    image_width = "abc"
    num_images = 10
    output_path = temporary_directory

    execution = subprocess.run([
        "python", "-m", "number-generator-script",
        "generate-phone-numbers",
        "--min-space", f"{min_space}",
        "--max-space", f"{max_space}",
        "--image-width", f"{image_width}",
        "--output-path", f"{output_path}",
        "--num-images", f"{num_images}"
    ])

    assert (execution.returncode != 0)

def test_case_9():
    """
    Checks the CLI-2 fails with invalid input.
    """
    min_space = 2
    max_space = 4
    image_width = 50
    num_images = 3
    output_path = "abc"

    execution = subprocess.run([
        "python", "-m", "number-generator-script",
        "generate-phone-numbers",
        "--min-space", f"{min_space}",
        "--max-space", f"{max_space}",
        "--image-width", f"{image_width}",
        "--output-path", f"{output_path}",
        "--num-images", f"{num_images}"
    ])

    assert (execution.returncode != 0)

def test_case_10(temporary_directory):
    """
    Checks the CLI-2 fails with invalid input.
    """
    min_space = 2
    max_space = 4
    image_width = 50
    num_images = 0
    output_path = temporary_directory

    execution = subprocess.run([
        "python", "-m", "number-generator-script",
        "generate-phone-numbers",
        "--min-space", f"{min_space}",
        "--max-space", f"{max_space}",
        "--image-width", f"{image_width}",
        "--output-path", f"{output_path}",
        "--num-images", f"{num_images}"
    ])

    assert (execution.returncode != 0)