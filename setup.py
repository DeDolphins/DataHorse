import os
import re
import setuptools
from typing import AnyStr, List


def read_file(path_parts: List[str], encoding: str = "utf-8") -> AnyStr:
    """
    Read a file from the project directory
    Args:
        path_parts: List of parts of the path to the file
        encoding: Encoding of the file
    Returns:
        Content of the file as a string
    """
    with open(
        os.path.join(os.path.dirname(__file__), *path_parts), "r", encoding=encoding
    ) as file:
        return file.read()


version_contents = read_file(["datahorse", "__version__.py"])
about = {}

for key in [
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
]:
    key_match = re.search(f"{key} = ['\"]([^'\"]+)['\"]", version_contents)
    if key_match:
        about[key] = key_match.group(1)

readme = read_file(["README.md"])

# Include only pandas and groq
required_packages = [
    "pandas",
    "groq",
    "numpy",
    "matplotlib",
    "seaborn",
    "scikit-learn"
]

extras = {
    "test": [
        "black",
        "coverage",
        "flake8",
        "mock",
        "pydocstyle",
        "pytest",
        "pytest-cov",
        "tox",
    ]
}

setuptools.setup(
    name=about.get("__title__", "unknown"),
    version=about.get("__version__", "0.0.0"),
    description=about.get("__description__", "unknown"),
    long_description=readme,
    author=about.get("__author__", "unknown"),
    author_email=about.get("__author_email__", "unknown"),
    url=about.get("__url__", "unknown"),
    packages=setuptools.find_packages("datahorse"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    license=about.get("__license__", "unknown"),
    package_dir={"": "datahorse"},
    package_data={"": ["*.txt"]},
    extras_require=extras,
    install_requires=required_packages,
    long_description_content_type="text/markdown",
    python_requires=">=3.7.0",
)
