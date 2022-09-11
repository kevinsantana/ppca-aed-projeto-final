# Source: https://packaging.python.org/guides/distributing-packages-using-setuptools/

from os import path
from setuptools import find_packages, setup

run_requirements = [
    "black==22.8.0",
    "click==8.1.3",
    "loguru==0.6.0",
    "mypy-extensions==0.4.3",
    "numpy==1.23.2",
    "pathspec==0.10.1",
    "platformdirs==2.5.2",
    "pyclean==2.2.0",
    "tomli==2.0.1",
]

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as readme:
    long_description = readme.read()

setup(
    name="Projeto Final AED",
    version="1.0.0",
    author="Kevin de Santana Araujo",
    author_email="kevin_santana.araujo@hotmail.com",
    packages=find_packages(exclude=["docs", "tests"]),
    url="https://github.com/kevinsantana/ppca-aed-projeto-final",
    description="Projeto Final AED",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=run_requirements,
    python_requires=">=3.10.4",
)
