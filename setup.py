from setuptools import find_packages, setup

version = "0.1"

requirements = [
    "matplotlib",
]

info = {
    "name": "rsmf",
    "version": version,
    "maintainer": "Johannes Jakob Meyer",
    "maintainer_email": "mail@johannesjakobmeyer.com",
    "url": "https://github.com/johannesjmeyer/rsmf",
    "packages": find_packages(where="."),
    "description": "rsmf (right-size my figures) helps you prepare publication-ready figures with matplotlib.",
    "long_description": open("README.md").read(),
    long_description_content_type="text/markdown",
    "provides": ["rsmf"],
    "install_requires": requirements,
    "classifiers": [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
    ],
}

setup(**(info))
