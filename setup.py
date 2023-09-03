from setuptools import setup

requires = [
    "numpy==1.22.2",
    "opencv-python==4.5.5.62",
    "click==8.0.4",
    "tqdm==4.62.3",
    "python-mnist==0.7",
    "matplotlib==3.5.1",
    "pytest==7.4.0"
]

setup(
    name="Image Generator",
    version="1.0",
    description="Image Generation Python Package",
    author="Jubin Ben",
    author_email="jubinben@gmail.com",
    url="https://jubinben98.github.io/Portfolio/",
    install_requires=requires,
    package_dir={"": "src/"},
    python_requires=">=3.9"
)