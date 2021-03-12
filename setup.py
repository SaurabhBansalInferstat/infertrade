#!/usr/bin/env python3
"""
infertrade setup.py file

Created by: Joshua Mason
Created date: 12/03/2021
"""

# Python standard library
import re

from os import walk
from pathlib import Path

# Third library (not InferStat)
from setuptools import  find_packages, setup

# Hardcoded variables
PROJECT_NAME = "infertrade"
PROJECT_DESCRIPTION = "Implementation of algorithmic trading functions"
BLACKLIST_DIRS = ["example_scripts"]

this_directory = Path(__file__).cwd()


def get_long_description(filename: str = "README.md") -> str:
    """Returns a long repository description read from file."""
    try:
        with open(Path.joinpath(this_directory, filename)) as f:
            long_description = "\n" + f.read()
    except FileNotFoundError:
        long_description = ""
    return long_description


def get_pkg_list(requirement_file: str) -> list:
    """Returns a list of packages requirements from listed file."""
    with open(Path.joinpath(this_directory, requirement_file)) as f:
        packages_full_list = [pkg.strip() for pkg in f.readlines() if not pkg.startswith("#")]
        list_of_packages_with_versions = [pkg for pkg in packages_full_list if pkg]
    return list_of_packages_with_versions


def get_version(filename: str = "_version.py") -> str:
    """Returns the package version number as a string by searching and reading the _version.py file."""
    for dirpath, _, filenames in walk(".", topdown=True):
        if ".gitignore" in filenames:
            with open(".gitignore") as _f:
                gitignore = [file.strip() for file in _f.readlines() if not re.search(r"\#|\*", file)]

        if any(pattern for pattern in gitignore + BLACKLIST_DIRS if re.search(pattern, dirpath)):
            continue
        for file in filenames:
            if filename in file:
                file_path = Path().joinpath(dirpath, filename)
    try:
        assert file_path.is_file()
        with open(file_path) as f:
            _version_info = "".join([i.strip() for i in f.readlines() if i.startswith("_")])
            _version_info = _version_info.replace(" ", "").replace('"', "").replace('"', "")
            about = dict([_version_info.split("=")])  # noqa: C406
    except FileNotFoundError:  # TODO - probably should be expected error types.
        raise RuntimeError(f"Unable to find version information in '{file_path}'.")
    else:  # TODO - currently this can't trigger as prior exception catches all errors.
        return about["__version__"]


# Get a list of packages as defined in file
package_requirements = get_pkg_list("requirements.txt")
dev_requirements = get_pkg_list("requirements-dev.txt")

# Setting up basic parameters of infertrade library
setup(
    name=PROJECT_NAME,
    version=get_version(),
    description=PROJECT_DESCRIPTION,
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url=f"https://github.com/ProjectOPTimize/{PROJECT_NAME}",
    author="InferStat Ltd",
    author_email="support@inferstat.com",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=package_requirements,
    extras_require={"dev": dev_requirements},
    tests_require=["pytest"],
    python_requires=">=3.7.0",
    classifiers=[
        "License :: OSI Approved :: InferStat License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    zip_safe=False,
)
