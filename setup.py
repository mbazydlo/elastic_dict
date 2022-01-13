import pathlib
from setuptools import setup

__version__ = "0.3.3"


DIRNAME = pathlib.Path(__file__).parent
README = (DIRNAME / "README.md").read_text()

setup(
    name="elasticdict",
    version=__version__,
    description="Library serving ElasticDict - dictionary like type with elastic values searching",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/mbazydlo/elastic_dict",
    author="Marcin Bazydło",
    author_email="marcin.p.bazydlo@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
    ],
    packages=["elasticdict"],
    include_package_data=True,
)
