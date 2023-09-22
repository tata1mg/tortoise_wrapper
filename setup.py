from setuptools import find_packages, setup

with open("requirements/base.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="tortoise_wrapper",
    version="1.0.0",
    author="1mg",
    author_email="devops@1mg.com",
    url="https://github.com/tata1mg/tortoise_wrapper/",
    description="Wrapper for tortoise",
    packages=find_packages(),
    install_requires=requirements,
)
