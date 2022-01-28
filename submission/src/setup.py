#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

requirements = ["Click>=7.1.2", "scipy==1.7.1", "numpy==1.21.2"]

test_requirements = [
    "pytest>=3",
]

setup(
    author="Challenge Authors",
    author_email="filip.igor.pawlowski@huawei.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    description="Hypergraph Partitioning Starter Kit",
    entry_points={"console_scripts": ["hg_tools=hg_tools.cli:main",],},
    install_requires=requirements,
    license="Apache Software License 2.0",
    include_package_data=True,
    keywords="hg_tools",
    name="hg_tools",
    packages=find_packages(include=["hg_tools", "hg_tools.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://gitlab.huaweirc.ch/zrc-von-neumann-lab/spatial-computing/university-challenge-2021/",
    version="0.1.0",
    zip_safe=False,
)
